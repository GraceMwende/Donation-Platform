from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser,BenefactorsStories


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email','user_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email','user_name')

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = BenefactorsStories
        fields = '__all__'
