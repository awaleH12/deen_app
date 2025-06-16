from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, UserForm  # Import the custom form and profile forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import uuid
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required

# Registration view

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require email verification
            messages.info(request, 'If you did not receive the verification email, <a href="' + reverse('accounts:resend_verification_email') + '">click here to request a new one</a>.')
            user.save()
            # Create profile with unique email token
            token = str(uuid.uuid4())
            while Profile.objects.filter(email_token=token).exists():
                token = str(uuid.uuid4())
            Profile.objects.create(user=user, email_token=token)
            # Build verification URL
            verify_url = request.build_absolute_uri(
                reverse('accounts:verify_email') + '?' + urlencode({'token': token})
            )
            try:
                send_mail(
                    'Verify your email',
                    f'Thank you for registering. Please verify your email by clicking the following link: {verify_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f'An error occurred while sending the verification email: {str(e)}')
                return redirect(reverse('accounts:register'))
            messages.success(request, 'You have successfully registered. Please verify your email to activate your account.')
            request.session['show_resend_verification'] = True
            request.session['registered_email'] = user.email
            return redirect(reverse('accounts:login'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    # Render the registration template with the form instance passed in the context dictionary
    return render(request, 'deen_app/accounts/register.html', {'form': form})

# Login view

def login_view(request):
    resend_email = False
    entered_email = None
    show_resend_verification = request.session.pop('show_resend_verification', False)
    registered_email = request.session.pop('registered_email', None)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        user = None
        # Try to get user by username or email
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                user = None
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('deen_app:dashboard'))
        else:
            # Check if user exists and is inactive
            if user and not user.is_active:
                resend_email = True
                entered_email = user.email
                messages.error(request, 'Your account is inactive. Please verify your email. You can resend the verification email below.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'deen_app/accounts/login.html', {
        'form': form,
        'resend_email': resend_email,
        'entered_email': entered_email,
        'show_resend_verification': show_resend_verification,
        'registered_email': registered_email,
    })

# Logout view

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect(reverse('accounts:login'))

def google_login_redirect(request):
    if request.user.is_authenticated:
        return redirect(reverse('deen_app:dashboard'))
    return redirect(reverse('accounts:login'))

def verify_email_view(request):
    token = request.GET.get('token')
    try:
        profile = Profile.objects.get(email_token=token)
        user = profile.user
        user.is_active = True
        user.save()
        profile.email_token = ''  # Invalidate token
        profile.save()
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect(reverse('accounts:login'))
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid or expired verification link. You can request a new verification email.')
        return redirect(reverse('accounts:resend_verification_email'))
    except Exception:
        messages.error(request, 'Invalid or expired verification link.')
        return redirect(reverse('accounts:login'))

# Profile view

@login_required
def profile_view(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect(reverse('accounts:profile'))
    return render(request, 'deen_app/accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                # Generate or get token
                profile = Profile.objects.get(user=user)
                if not profile.email_token:
                    import uuid
                    profile.email_token = str(uuid.uuid4())
                    profile.save()
                verify_url = request.build_absolute_uri(
                    reverse('accounts:verify_email') + '?' + urlencode({'token': profile.email_token})
                )
                send_mail(
                    'Verify your email',
                    f'Please verify your email: {verify_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, 'Verification email sent. Please check your inbox.')
            else:
                messages.info(request, 'Account is already active.')
        except User.DoesNotExist:
            messages.error(request, 'No user with that email.')
    return render(request, 'deen_app/accounts/resend_verification.html')
