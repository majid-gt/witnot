# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import UserResponse, Question, ExamSession, Feedback

# --------------------------
# LOGIN SERIALIZER
# --------------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")


# --------------------------
# START EXAM SERIALIZER
# --------------------------
class StartExamSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()


# --------------------------
# QUESTION SERIALIZER
# --------------------------
class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    user_answer = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'user_answer', 'image_url']

    def get_options(self, obj):
        return {
            "A": obj.option_a,
            "B": obj.option_b,
            "C": obj.option_c,
            "D": obj.option_d
        }

    def get_user_answer(self, obj):
        # Optimized for Redis: use 'answers_cache' if passed in context
        session = self.context.get('session')
        answers_cache = self.context.get('answers_cache', {})  # {question_id: selected_answer}

        if answers_cache.get(obj.id):
            return answers_cache[obj.id]

        if session:
            response = UserResponse.objects.filter(exam_session=session, question=obj).first()
            return response.selected_answer if response else None
        return None

    def get_image_url(self, obj):
        return obj.image_url if obj.image_url else None


# --------------------------
# USER RESPONSE UPDATE SERIALIZER
# --------------------------
class UserResponseUpdateSerializer(serializers.Serializer):
    selected_answer = serializers.ChoiceField(choices=['A', 'B', 'C', 'D', 'N'])
    warnings_count = serializers.IntegerField(min_value=0)

    def validate(self, data):
        if 'selected_answer' not in data:
            raise serializers.ValidationError("selected_answer is required")
        if 'warnings_count' not in data:
            raise serializers.ValidationError("warnings_count is required")
        return data


# --------------------------
# USER RESPONSE SERIALIZER
# --------------------------
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ['exam_session', 'question', 'selected_answer', 'is_penalized']


# --------------------------
# FEEDBACK SERIALIZER
# --------------------------
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'rating', 'feedback_text', 'submitted_at']
