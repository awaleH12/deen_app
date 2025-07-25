from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Profile
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_('First name'),
        widget=forms.TextInput(attrs={'placeholder': _('First name')}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_('Last name'),
        widget=forms.TextInput(attrs={'placeholder': _('Last name')}),
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={'placeholder': _('Username')}),
        validators=[RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'))]
    )
    email = forms.EmailField(
        required=True,
        label=_('Email'),
        widget=forms.EmailInput(attrs={'placeholder': _('Email')}),
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password')}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter your username'),
            'class': 'form-control',
            'id': 'id_username',
        }),
        max_length=150,
        required=True,
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Enter your password'),
            'class': 'form-control',
            'id': 'id_password',
        }),
        required=True,
    )
