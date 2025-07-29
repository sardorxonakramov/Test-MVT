from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import random, string

User = settings.AUTH_USER_MODEL

class Test(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=5, unique=True, blank=True)
    duration = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1)],
        help_text="Test davomiyligi (daqiqada)"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if not Test.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True, help_text="LaTeX formatida savol matni")
    image = models.ImageField(upload_to='teachers/questions/', blank=True, null=True)
    warning = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text or f"Question #{self.id}"


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=True, help_text="LaTeX formatida variant matni")
    image = models.ImageField(upload_to='teachers/options/', blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text or f"Option #{self.id}"
