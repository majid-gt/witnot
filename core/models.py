from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    MARK_CHOICES = [(1, '1 Mark'), (2, '2 Marks')]
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    marks = models.IntegerField(choices=MARK_CHOICES)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.marks} mark)"

class IOTQuestion(models.Model):
    MARK_CHOICES = [(1, '1 Mark'), (2, '2 Marks')]
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    marks = models.IntegerField(choices=MARK_CHOICES)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.marks} mark)"

class ExamSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    started_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    warnings = models.IntegerField(default=0)
    total_penalties = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Exam for {self.user.username}"
class UserResponse(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(
    max_length=1,
    choices=[
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('N','Not Marked')
    ],
    default='N',  # default value
    blank=True,
    null=True
)
    is_penalized = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def is_correct(self):
        return self.selected_answer == self.question.correct_answer

    def __str__(self):
        return f"{self.exam_session.user.username} → {self.question.text[:30]} = {self.selected_answer or 'Not answered'}"

class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)

    def increment(self):
        self.attempts += 1
        self.save()
# models.py
from django.db import models

class Feedback(models.Model):
    RATING_CHOICES = [
        ('outstanding', 'Outstanding'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('bad', 'Bad'),
    ]

    rating = models.CharField(max_length=20, choices=RATING_CHOICES)
    feedback_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.feedback_text[:30]}"

# models.py


from django.db import models

class ExamConfig(models.Model):
    name = models.CharField(max_length=100, default="Default Exam")
    exam_start = models.DateTimeField(null=True, blank=True)
    submission_start = models.DateTimeField(null=True, blank=True)
    exam_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
