# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from Login.forms import SignUpForm  
from django.http import HttpResponseRedirect

from Logger.views import *

def signUpRequest(request):
    if request.user.is_authenticated():
        LogInfo(request.user.id, "User Already Logged In")
        return redirect('/dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
             
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                messages.success(request, 'Thanks for registration, you can now log in!')
                LogInfo(request.user.id, "User Succesfully Logged In")
                return redirect("/login")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                LogWarning(request.user.id, "User Inputted Invalid Captcha")
                return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()

    for field in form.fields:
        form.fields[field].widget.attrs.update({
        'class': 'form-control',
        'placeholder':''
        })    
    return render(request, 'register.html', {'form': form})

def custom_login(request):
    if request.user.is_authenticated():
        return redirect('/dashboard')
    else:
        return login(request)

