from django import forms
from .models import Test, Question, Option


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description", "duration"]
        widgets = {
            "duration": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "image", "warning"]
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control"}),
            "warning": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text", "image", "is_correct"]
        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "is_correct": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
