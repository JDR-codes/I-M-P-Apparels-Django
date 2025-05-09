from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .forms import RegisterUserForm, LoginUserForm, CustomPasswordResetForm,CustomSetPasswordForm
from .utils import send_verification_email

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_verification_email(
                user = user,
                request = request,
                subject = 'Verify your email',
                message = 'Click the link to verify your email: ',
                url_name = 'verify-email')
            messages.success(request, "Please verify your email.")
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})


def verify_email_view(request, uidb64, token):
    print(request)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully.")
        return redirect('email-verified')
    else:
        messages.error(request, "Invalid or expired link.")
        return redirect('email-verified')

def email_verified_view(request):
    return render(request,'email_verified.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginUserForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def custom_password_reset_view(request):
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_verification_email(
                    user=user,
                    request=request,
                    subject="Password Reset Request",
                    message="Click the link below to reset your password:\n",
                    url_name = 'password_reset_confirm'
                )
            except User.DoesNotExist:
                pass  # For security, do not reveal if email exists
            messages.success(request, "If an account with that email exists, a reset link has been sent. Please check your inbox.")
            form = CustomPasswordResetForm()
    else:
        form = CustomPasswordResetForm()
    return render(request, 'pass_reset_form.html', {'form': form})

def custom_password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully. You can now log in.")
                return redirect('login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'reset_confirm_form.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return render(request, 'reset_confirm_form.html', {})