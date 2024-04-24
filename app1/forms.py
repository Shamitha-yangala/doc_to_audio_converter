from django import forms
from .models import UserUpload

class UserUploadForm(forms.ModelForm):
    class Meta:
        model = UserUpload
        fields = ['user_name', 'title', 'description', 'attachment']
