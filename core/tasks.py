# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import ExamSession, UserResponse

@shared_task
def auto_submit_exam(session_id):
    try:
        session = ExamSession.objects.get(id=session_id)
    except ExamSession.DoesNotExist:
        return

    if session.is_completed:
        return

    total_score = 0
    for resp in UserResponse.objects.filter(exam_session=session):
        if resp.is_correct():
            total_score += resp.question.marks

    # Deduct penalties based on warnings
    penalty_marks = 0.5 * max(0, session.warnings - 5)
    total_score -= penalty_marks
    if total_score < 0:
        total_score = 0

    session.total_score = total_score
    session.is_completed = True
    session.save()
