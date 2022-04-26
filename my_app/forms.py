from django import forms
from django.contrib.auth.models import User


class UploadFileForm(forms.Form):
    file = forms.FileField()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email','is_active']