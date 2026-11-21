from django import forms
import os
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from questions.models import Profile

def validate_avatar(avatar):
    if not avatar.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        raise forms.ValidationError('Only JPG, PNG or WEBP')
    if avatar.size > 2 * 1024 * 1024:
        raise forms.ValidationError('Max 2 MB')

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'loginl', 'placeholder': 'Enter your login here...'}),
        label = "login"
    )
    password = forms.CharField(
        required=True,
        widget = forms.PasswordInput(attrs={'id': 'passwordl', 'placeholder': 'Enter your password here...'}),
        label = "password"
    )

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'id': 'emails', 'placeholder': 'Enter your email here...'}),
        label = "Email"
    )
    nickname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'nicknames', 'placeholder': 'Enter your nickname here...'}),
        label = "Nickname"
    )
    username = forms.CharField(
        required=True,
        widget = forms.TextInput(attrs={'id': 'logins', 'placeholder': 'Enter your login here...'}),
        label = "Login"
    )
    avatar = forms.ImageField(
        required=False,
        validators=[validate_avatar],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        label = "Upload avatar"
    )
    password1 = forms.CharField(
        required=True,
        help_text="",
        widget=forms.PasswordInput(attrs={'id': 'passwords1', 'placeholder': 'Enter your password here...'}),
        label = "Password"
    )
    password2 = forms.CharField(
        required=True,
        help_text="",
        widget=forms.PasswordInput(
            attrs={'id': 'passwords2', 'placeholder': 'Repeat your password here...'}),
        label="Repeat password"
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Profile.objects.create(
                user=user,
                nickname=self.cleaned_data.get('nickname', ''),
                avatar=self.cleaned_data.get('avatar'),
            )
        return user

class CustomProfileForm(forms.ModelForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'id': 'emailp'})
    )
    nickname = forms.CharField(
        label="NickName",
        required=True,
        widget=forms.TextInput(attrs={'id': 'nicknamep'})
    )
    avatar = forms.ImageField(
        label="Upload avatar",
        validators=[validate_avatar],
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'id_avatar', 'accept': 'image/*'})
    )
    class Meta:
        model = Profile
        fields = ('nickname', 'avatar')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user: self.fields['email'].initial = self.instance.user.email
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        if commit:
            profile.user.save()
            profile.save()
        return profile