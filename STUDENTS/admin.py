from django.contrib import admin
from .models import StudentTest, StudentAnswer


@admin.register(StudentTest)
class StudentTestAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'completed', 'started_at')
    list_filter = ('completed', 'test')
    search_fields = ('student__username', 'test__title')
    ordering = ('-started_at',)


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student_test', 'question_text', 'selected_option', 'is_correct')
    list_filter = ('is_correct', 'question__test')
    search_fields = ('student_test__student__username', 'question__text')

    def question_text(self, obj):
        return obj.question.text
    question_text.short_description = 'Savol'
