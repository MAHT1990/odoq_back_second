from django.contrib import admin
from .models import *

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
        'created_at',
    ]

# Register your models here.

# Register your models here.
