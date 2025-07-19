from django.db import models
from django.contrib.auth.models import User
from django import forms

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_token = models.CharField(max_length=64, blank=True)  # For email verification
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']  # Add other fields as needed
