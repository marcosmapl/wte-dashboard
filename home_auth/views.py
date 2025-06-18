from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import WineUser
from django.contrib import messages
# from django.core.mail import send_mail
# from django.utils.crypto import get_random_string


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        
        # Create the user
        user = WineUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_active=True,
        )
        user.is_staff =False
        user.is_superuser = False
        user.is_booking_agent = True
        user.is_general_manager = False
        user.is_it_manager = False
        user.is_read_only = False

        user.save()  # Save the user with the assigned role
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('dashboard_general')  # Redirect to the index or home page
    return render(request, 'authentication/register.html')  # Render signup template


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard_general')
            
            # # Redirect user based on their role
            # if user.is_admin:
            #     return redirect('admin_dashboard')
            # elif user.is_teacher:
            #     return redirect('teacher_dashboard')
            # elif user.is_student:
            #     return redirect('dashboard')
            # else:
            #     messages.error(request, 'Invalid user role')
            #     return redirect('index')  # Redirect to index in case of error 
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'authentication/login.html')  # Render login template


# def forgot_password_view(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         user = WineUser.objects.filter(email=email).first()
        
#         if user:
#             token = get_random_string(32)
#             reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
#             reset_request.send_reset_email()
#             messages.success(request, 'Reset link sent to your email.')
#         else:
#             messages.error(request, 'Email not found.')
    
#     return render(request, 'authentication/forgot-password.html')  # Render forgot password template


# def reset_password_view(request, token):
#     reset_request = PasswordResetRequest.objects.filter(token=token).first()
    
#     if not reset_request or not reset_request.is_valid():
#         messages.error(request, 'Invalid or expired reset link')
#         return redirect('index')

#     if request.method == 'POST':
#         new_password = request.POST['new_password']
#         reset_request.user.set_password(new_password)
#         reset_request.user.save()
#         messages.success(request, 'Password reset successful')
#         return redirect('index')

#     return render(request, 'authentication/reset_password.html', {'token': token})  # Render reset password template


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
