# urls.py
from django.urls import path
from .views import LoginAPI,ExamDataAPI,UpdateQuestionAPI,FinalSubmitAPI,FeedbackAPI,EndExpiredExamsAPI, LogoutAPI
from rest_framework_simplejwt.views import TokenRefreshView
import misstantra.settings as settings
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', LogoutAPI.as_view(), name='logout'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/exam/<str:rollno>/', ExamDataAPI.as_view(), name='exam-data'),
    path('api/exam/<str:rollno>/question/<int:question_id>/update/', UpdateQuestionAPI.as_view(), name='update-question'),
    path('api/exam/<str:rollno>/submit/', FinalSubmitAPI.as_view(), name='final-submit'),
    path('api/feedback/', FeedbackAPI.as_view(), name='feedback-api'),
    path('api/admin/end-expired-exams/', EndExpiredExamsAPI.as_view(), name='end_expired_exams'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)