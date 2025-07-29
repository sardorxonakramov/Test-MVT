from django import forms
from .models import Test, Question, Option


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description", "duration"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "duration": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "image", "warning"]
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": r"Masalan: x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}"
            }),
            "warning": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Eslatma (ixtiyoriy)"
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text", "image", "is_correct"]
        widgets = {
            "text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": r"Masalan: x = \sqrt{a^2 + b^2}"
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_correct": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
