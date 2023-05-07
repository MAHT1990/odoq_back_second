from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

@admin.register(SmsHistory)
class SmsHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'sms_type',
        'send_to',
        'content',
        'is_succeed',
        'sent_at',
    ]
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'season',
        'img',
        'text',
        'created_at',
        'updated_at',
    ]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code',
        'season',
        'img_tag',
        'answer',
        'upload_datetime',
        'answer_count',
        'solve_count',
        'created_at',
    ]
    list_editable = [
        'answer',
        'upload_datetime',
    ]

    def img_tag(self, question):
        if question.img:
            return mark_safe(f'<a href="{question.img.url}" target="_blank" rel="noopener noreferrer"><img src="{question.img.url}" style="width:250px"/></a>')
    class Meta:
        ordering = ["-upload_datetime"]

@admin.register(AnswerHistory)
class AnswerHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'question',
        'user_name',
        'answer',
        'isSolved',
        'created_at',
    ]
    list_display_links = [
        'user_name',
    ]
    def user_name(self, answer_history):
        return answer_history.user.name
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'content',
        'like_count',
        'created_at',
        'updated_at',
        'blind',
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'post',
        'content',
        'created_at',
        'updated_at',
    ]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'name',
        'phone',
        'grade',
        'created_at',
        'accept_sms',
    ]
    list_editable = [
        'grade',
        'accept_sms',
    ]

# Register your models here.

# Register your models here.
