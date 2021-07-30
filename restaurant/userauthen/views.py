from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from django.conf import settings
from django.contrib import messages
from .forms import SignUpForm


def home(request):
    return render(request, 'auth/home.html')


def signup(request):
    print("hello")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print("valid")
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    else:
        print("invalid")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
        form = SignUpForm()

    return render(request, 'auth/signup.html', {'form': form})
