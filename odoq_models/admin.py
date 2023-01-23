from django.contrib import admin
from .models import *

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'season',
        'img',
        'answer',
        'upload_datetime',
        'answer_count',
        'solve_count',
        'created_at',
    ]

# Register your models here.

# Register your models here.
