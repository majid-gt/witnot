# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .serializers import (
    LoginSerializer,
    UserResponseUpdateSerializer,
    QuestionSerializer,
    FeedbackSerializer
)
from .models import LoginAttempt, ExamSession, Question, UserResponse, ExamConfig
from .utils import generate_user_exam
from .utils import get_exam_session, set_exam_session, delete_exam_session
from rest_framework.permissions import IsAdminUser
from datetime import datetime

import pytz

IST = pytz.timezone('Asia/Kolkata')

def get_exam_times():
    """
    Safely fetch exam configuration from DB.
    This prevents Django startup crashes before migrations.
    """
    config = ExamConfig.objects.first()
    if not config:
        return None, None, None

    exam_start = config.exam_start.astimezone(IST)
    submission_start_ist = config.submission_start.astimezone(IST)
    exam_end = config.exam_end.astimezone(IST)

    return exam_start, submission_start_ist, exam_end


max_attempts = 10


# --------------------------
# LOGIN API
# --------------------------
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            # 🔹 Login attempts
            attempt, _ = LoginAttempt.objects.get_or_create(user=user)
            if attempt.attempts >= 3000:
                return Response(
                    {"error": "Maximum login attempts exceeded. Contact administrator."},
                    status=status.HTTP_403_FORBIDDEN
                )
            attempt.increment()

            # 🔑 JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "message": "Login successful",
                "username": user.username,
                "attempts_left": 5 - attempt.attempts,
                "access": access_token,
                "refresh": refresh_token
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------
# EXAM DATA API
# --------------------------
class ExamDataAPI(APIView):
    def get(self, request, rollno):
        user = get_object_or_404(User, username=rollno)

        # Check Redis first
        exam_start, submission_start_ist, exam_end = get_exam_times()

        if not exam_start:
            return Response({"error": "Exam configuration missing"}, status=500)

        print("Exam Config Times:", exam_start, exam_end)        

        # Get or create exam session
        session, created = ExamSession.objects.get_or_create(
            user=user,
            defaults={'end_time': exam_end}
        )

        if session.completed:
            return Response({"error": "Exam already submitted"}, status=403)

        # Increment login attempts only if new
        if created:
            login_record, _ = LoginAttempt.objects.get_or_create(user=user)
            if login_record.attempts >= 8:
                return Response({"error": "Login limit exceeded. Contact admin."}, status=403)
            login_record.increment()

        # Assign questions if new session
        if created or session.questions.count() == 0:
            selected_qs = generate_user_exam()
            session.questions.set(selected_qs)
            session.save()

        # Timer
    

        # Serialize questions
        questions = session.questions.all()
        serializer = QuestionSerializer(questions, many=True, context={'session': session})
        response_data = {
            "username": user.username,
            "start_time": exam_start,
            "end_time": exam_end,
            "warnings": session.warnings,
            "penalties": session.total_penalties,
            "questions": serializer.data
        }

        # Cache in Redis until exam_end
        

        return Response(response_data)


# --------------------------
# UPDATE QUESTION API
# --------------------------
class UpdateQuestionAPI(APIView):
    def post(self, request, rollno, question_id):
        user = get_object_or_404(User, username=rollno)
        session = get_object_or_404(ExamSession, user=user)
        question = get_object_or_404(Question, id=question_id)
        user_response, _ = UserResponse.objects.get_or_create(
            exam_session=session,
            question=question
        )

        serializer = UserResponseUpdateSerializer(data=request.data)
        if serializer.is_valid():
            selected_answer = serializer.validated_data['selected_answer']
            warnings_count = serializer.validated_data['warnings_count']

            # Update DB
            user_response.selected_answer = selected_answer
            user_response.save()
            session.warnings += warnings_count
            session.total_penalties = max(0, (session.warnings - 5) * 0.5)
            session.save()

            # Update Redis
            cached = get_exam_session(user.id)
            if cached:
                cached['warnings'] = session.warnings
                cached['penalties'] = session.total_penalties
                # Update answer in cached questions
                for q in cached['questions']:
                    if q['id'] == question.id:
                        q['user_answer'] = selected_answer
                set_exam_session(user.id, cached, timeout=max(int((session.end_time - timezone.now()).total_seconds()), 0))

            return Response({
                "message": "Answer updated successfully",
                "question_id": question.id,
                "selected_answer": user_response.selected_answer,
                "penalty_score": session.total_penalties,
                "total_warnings": session.warnings
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------
# FINAL SUBMIT API
# --------------------------
class FinalSubmitAPI(APIView):
    def post(self, request, rollno):
        user = get_object_or_404(User, username=rollno)
        session = get_object_or_404(ExamSession, user=user)
        warnings = request.data.get("totalWarnings", 0)
        session.warnings = warnings
        session.total_penalties = max(0, (session.warnings - 5) * 0.5)

       
        session.completed = True
        session.end_time = timezone.now()
        session.save()

        # Remove from Redis
        delete_exam_session(user.id)

        # Calculate scores
        responses = UserResponse.objects.filter(exam_session=session)
        total_marks = sum(resp.question.marks for resp in responses if resp.is_correct())
        penalty = max(0, (session.warnings - 5) * 0.5)
        final_score = max(0, total_marks - penalty)

        summary = [{
            "question_id": resp.question.id,
            "selected_answer": resp.selected_answer,
            "correct_answer": resp.question.correct_answer,
            "is_correct": resp.is_correct(),
            "marks": resp.question.marks
        } for resp in responses]

        return Response({
            "message": "Exam submitted successfully",
            "username": user.username,
            "total_questions": responses.count(),
            "total_marks": total_marks,
            "warnings": session.warnings,
            "penalty_score": penalty,
            "final_score": final_score,
            "responses": summary
        })


# --------------------------
# FEEDBACK API
# --------------------------
class FeedbackAPI(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Feedback submitted successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# --------------------------
# END EXPIRED EXAMS API
# --------------------------
class EndExpiredExamsAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        expired_sessions = ExamSession.objects.filter(completed=False)
        count = 0
        for session in expired_sessions:
            session.completed = True
            session.save()
            # Remove from Redis if exists
            delete_exam_session(session.user.id)
            count += 1

        return Response({"message": f"{count} exam session(s) successfully ended."})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # blacklist this refresh token

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated

class DashboardAPI(APIView):
    permission_classes = [IsAuthenticated]  # only logged-in users can see

    def get(self, request):
        user = get_object_or_404(User, username=request.user)
        session = ExamSession.objects.filter(user=user).first()

        # Get exam times safely from DB
        exam_start, submission_start_ist, exam_end = get_exam_times()

        if not exam_start:
            return Response(
                {"error": "No exam configured"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Determine exam status
        if session is None:
            exam_status = "none"
        else:
            if session.completed is False:
                exam_status = "ongoing"
            else:
                exam_status = "completed"

        from datetime import datetime
        IST = pytz.timezone('Asia/Kolkata')
        now_ist = datetime.now(IST)

        if now_ist > exam_end:
            exam_status = "completed"

        print(exam_status)

        return Response({
            "exam_name": "Power BI Exam",
            "exam_start": exam_start,
            "exam_status": exam_status,
            "exam_end": exam_end,
        }, status=status.HTTP_200_OK)