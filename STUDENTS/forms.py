from django import forms

class TestCodeForm(forms.Form):
    code = forms.CharField(label='Test kodi', max_length=5)
