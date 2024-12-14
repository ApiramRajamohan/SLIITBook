from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate,login
from random import randint

def Register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            #Now save the user
            new_user.save()
            log_user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            if log_user is not None:
                login(request, log_user)
            return JsonResponse({'status': 'success'})
    else:
        user_form = UserRegistrationForm()
    return HttpResponse("Register Page")

def Login(request):
    return HttpResponse("LoginPage")

def Profile(request):
    return HttpResponse("ProfilePage")


