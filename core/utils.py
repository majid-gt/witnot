import random
from django.core.cache import cache
from django.utils import timezone
from .models import Question, ExamSession, UserResponse

# --------------------------
# Generate Random Exam
# --------------------------
def generate_user_exam():
    """
    Generate a random set of questions: 20 x 1-mark, 20 x 2-mark
    """
    one_mark_qs = list(Question.objects.filter(marks=1).order_by('-id').values_list('id', flat=True)[:100])
    


    selected_questions = random.sample(one_mark_qs, 50) 
    random.shuffle(selected_questions)
    return selected_questions


# --------------------------
# Redis Helpers
# --------------------------
def set_exam_session(user_id, data, timeout=None):
    """
    Save a user's exam session in Redis.
    """
    key = f"exam_session:{user_id}"
    cache.set(key, data, timeout)
    return key


def get_exam_session(user_id):
    """
    Fetch a user's exam session from Redis.
    If missing, rebuild from DB.
    """
    key = f"exam_session:{user_id}"
    cached = cache.get(key)
    if cached:
        return cached

    # Fallback: rebuild from DB if exists
    try:
        session = ExamSession.objects.get(user_id=user_id, completed=False)
        questions = session.questions.all()
        cached = {
            "username": session.user.username,
            "end_time": session.end_time,
            "warnings": session.warnings,
            "penalties": session.total_penalties,
            "questions": [
                {
                    "id": q.id,
                    "user_answer": UserResponse.objects.filter(exam_session=session, question=q).first().selected_answer
                    if UserResponse.objects.filter(exam_session=session, question=q).exists() else None
                }
                for q in questions
            ]
        }
        # Reset cache in Redis
        remaining_time = max(int((session.end_time - timezone.now()).total_seconds()), 0)
        cache.set(key, cached, timeout=remaining_time)
        return cached
    except ExamSession.DoesNotExist:
        return None


def delete_exam_session(user_id):
    """
    Remove a user's exam session from Redis after submission.
    """
    key = f"exam_session:{user_id}"
    cache.delete(key)
