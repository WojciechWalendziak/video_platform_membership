from .models import Profile, CustomUser
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ProfileForm(ModelForm):

	class Meta:
		model = Profile
		fields = ("name", "profile_type")


class UserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = CustomUser
		fields = ("email", "password1", "password2")


class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Email')

	class Meta:
		model = CustomUser
		fields = ("email", "password1")