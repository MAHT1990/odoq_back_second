from django.contrib import admin
from .models import *

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
        'img',
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

@admin.register(AnswerHistory)
class AnswerHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'question',
        'user',
        'answer',
        'isSolved',
        'created_at',
        'updated_at',
    ]
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
        'blind_text',
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
