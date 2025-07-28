from django.db import models
from django.contrib.auth import get_user_model
from TEACHERS.models import Test, Question, Option

User = get_user_model()


class StudentTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    # models.py ichida:
    attempt_number = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.student} - {self.test.title}"


class StudentAnswer(models.Model):
    student_test = models.ForeignKey(StudentTest, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.question.text} - {'To‘g‘ri' if self.is_correct else 'Noto‘g‘ri'}"

    @property
    def correct_option(self):
        return self.question.options.filter(is_correct=True).first()
