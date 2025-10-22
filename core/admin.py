from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# First, unregister the default registration (if already registered)
try:
    admin.site.unregister(User)
except Exception:
    # If it wasn't registered yet, ignore the error
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Customized User admin:
      - show username (roll), email, staff/active flags in list
      - search by username or email
      - ordering by username
      - keep default add/change behavior so passwords are hashed
    """
    # Columns displayed in the users list page
    list_display = ('username', 'email', 'is_staff', 'is_active')

    # Quick filters on the right
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    # Fields you can search for
    search_fields = ('username', 'email')

    # Default ordering
    ordering = ('username',)

    # Fieldsets used in the change user page (keeps Django defaults but you can reorder)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fieldsets used in the add user page (keeps Django add form layout)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Which fields are read-only in admin detail view (optional)
    readonly_fields = ('last_login', 'date_joined')

from django.contrib import admin
from .models import Question, ExamSession, UserResponse

# Register Question model
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'marks', 'correct_answer')
    search_fields = ('text',)
    list_filter = ('marks',)

# Register ExamSession model
@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'end_time', 'completed', 'warnings', 'total_penalties')
    list_filter = ('completed', 'started_at')
    search_fields = ('user__username',)
    filter_horizontal = ('questions',)  # Allows better selection of many-to-many Questions

# Register UserResponse model
@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('exam_session', 'question', 'selected_answer', 'is_penalized', 'submitted_at', 'is_correct_display')
    list_filter = ('is_penalized', 'submitted_at')
    search_fields = ('exam_session__user__username', 'question__text')

    def is_correct_display(self, obj):
        return obj.is_correct()
    is_correct_display.boolean = True
    is_correct_display.short_description = 'Correct?'
# core/admin.py
from django.contrib import admin
from .models import LoginAttempt

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'attempts')  # only these exist now
    search_fields = ('user__username',)

from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('rating', 'feedback_text', 'submitted_at')
    list_filter = ('rating', 'submitted_at')
    search_fields = ('feedback_text',)
    ordering = ('-submitted_at',)


# admin.py
from django import forms
from django.contrib import admin
from .models import ExamConfig
import pytz

IST = pytz.timezone('Asia/Kolkata')

class ExamConfigForm(forms.ModelForm):
    class Meta:
        model = ExamConfig
        fields = "__all__"

    def clean_exam_start(self):
        dt = self.cleaned_data['exam_start']
        if dt.tzinfo is None:  # naive datetime
            return IST.localize(dt)  # mark it as IST
        return dt

    def clean_submission_start(self):
        dt = self.cleaned_data['submission_start']
        if dt.tzinfo is None:
            return IST.localize(dt)
        return dt

    def clean_exam_end(self):
        dt = self.cleaned_data['exam_end']
        if dt.tzinfo is None:
            return IST.localize(dt)
        return dt

class ExamConfigAdmin(admin.ModelAdmin):
    form = ExamConfigForm

admin.site.register(ExamConfig, ExamConfigAdmin)
