from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import UserCreationForm,LoginForm
from django.contrib.auth import login,logout
from random import randint
import msal
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import Account
from django.core.cache import cache
import json
from .backends import EmailorUsernameBackend

# def MS_Auth(request):
#     app = msal.ConfidentialClientApplication(
#         settings.MICROSOFT_CLIENT_ID,
#         authority=f"https://login.microsoftonline.com/common",
#         client_credential=settings.MICROSOFT_CLIENT_SECRET
#     )
#     auth_url = app.get_authorization_request_url(
#         scopes=["User.Read", "openid", "email", "profile"],  # Define the scopes you need
#         redirect_uri=settings.MICROSOFT_REDIRECT_URI
#     )
#     return redirect(auth_url)

#https://learn.microsoft.com/en-us/entra/msal/python/getting-started/acquiring-tokens
#https://docs.djangoproject.com/en/5.1/topics/auth/default/
@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        user = Account.objects.filter(email = email).first()
        if user:
            return JsonResponse({'status':'Email already exist'}, status = 400)
        verificationcode = randint(100000,999999)
        # Send verification email
        cache.set(f'email_verification_code_{email}', verificationcode, timeout=300)
        subject = 'Your SLIITBook Email Verification Code'
        message = f'Your SLIITBook verification code is {verificationcode}.'
        print(cache.get(f'email_verification_code_{email}'))
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        print(f'email sent to {email}')
        return JsonResponse({'status': 'Verification code sent'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
#cache the code
@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        cached_code = cache.get(f'email_verification_code_{email}')
        #check whether cache memory matches
        if cached_code is None:
            return JsonResponse({'error' : 'Verification code expired or not sent'},status = 400)
        if str(cached_code) == code:
            # Code is correct, proceed with registration
            cache.delete(f'email_verification_code_{email}')  # Clear the cache after successful verification
            return JsonResponse({'status': 'Verification successful','success':True})
        else:
            return JsonResponse({'error': 'Invalid verification code'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def Register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_form = UserCreationForm(data)
        for x in data:
            print(x,data.get(x))
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save()
            new_user.set_password(user_form.cleaned_data['password'])
            #Now save the user  
            new_user.save()
            backend = EmailorUsernameBackend()
            log_user = backend.authenticate(request,username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            if log_user is not None:
                #Backend authenticated the credientials
                log_user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, log_user)
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid username/email or password'}, status=401)
        else:
            print(user_form.errors)
            return JsonResponse({'status': 'error', 'message': 'Invalid form'}, status=401)
            #error message has to be sent
    else:
        # authorization_header = request.headers.get("Authorization")
        # access_token = authorization_header.split(' ')[1]
        # if not access_token or not authorization_header.startswith('Bearer ') or not authorization_header:
        #     return JsonResponse({'error': 'Token is missing'}, status=400)
        # try:    
        #     # Use the access token to call Microsoft Graph API
        #     graph_api_url = "https://graph.microsoft.com/v1.0/me"
        #     headers = {'Authorization': f'Bearer {access_token}'}
        #     graph_response = requests.get(graph_api_url, headers=headers)
            
        #     if graph_response.status_code == 200:
        #         user_data = graph_response.json()
        #         email = user_data.get('mail', user_data.get('userPrincipalName'))  # Get email or fallback to userPrincipalName

        #         # Check if the email domain is correct
        #         if email.endswith('@mysliit.lk'):
        #             # Register the user or log them in here
        #             # Optionally, create a new user or check if the user exists in your database
        #             user = Account.objects.filter(email=email).first()
        #             if user:
        #                 login(request,user)
        #                 return JsonResponse({'status':'success'})
        #             else:
        #                 user_form = UserCreationForm()
        #                 return render(request, "Accounts/register.html", {"form": user_form, "email": email})
        #         else:
        #             return JsonResponse({'error': 'Invalid email domain'}, status=400)
        #     else:
        #         return JsonResponse({'error': 'Failed to retrieve user info'}, status=400)
        # except Exception as e:
        #     return JsonResponse({'error': 'Failed to acquire access token'}, status=400)
        return JsonResponse({'error': 'Invalid request'}, status=400)

def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            #authenticate using custom backend
            user = EmailorUsernameBackend.authenticate(request,username = username_or_email,password=password)
            if user is not None:
                login(request,user)
                return JsonResponse({'status':'success'})
            else:
                #error message has to be sent
                return JsonResponse({'status': 'error', 'message': 'Invalid username/email or password'}, status=400)
    else:        
        form = LoginForm()
    return render(request,"Accounts/login.html",{"title":"login","form":form}) # with error

@login_required
def Profile(request):
    return HttpResponse("ProfilePage")

@login_required
def Logout(request):
    logout(request)
    return redirect("login")

@login_required
def Delete(request):
    # Before deleting the user, show a confirmation message to avoid accidental deletions
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        return redirect("login")
    return render(request, "Accounts/delete_confirm.html", {"title": "Delete Account"})

@login_required
def Change_Password(request):
    return HttpResponse("changePassword")

@login_required
def Edit_Profile(request):
    return HttpResponse("Edit profile")