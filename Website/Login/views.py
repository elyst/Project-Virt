# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from Login.forms import SignUpForm  

def signUpRequest(request):
    if request.user.is_authenticated():
        return redirect('/dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            succes = 'Gelukt!'
            return custom_login(request, succes)
    else:
        form = SignUpForm()

    for field in form.fields:
        form.fields[field].widget.attrs.update({
        'class': 'form-control',
        'placeholder':''
        })    
    return render(request, 'register.html', {'form': form})

def custom_login(request, message=None):
    if request.user.is_authenticated():
        return redirect('/dashboard')
    else:
        return login(request)

