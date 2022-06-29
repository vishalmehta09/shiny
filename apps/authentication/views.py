# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from apps.authentication.models import NewUser
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def login_view(request):

    print(NewUser.objects.all().values())
    form = CustomUserLoginForm(request.POST )
    msg = None

    if request.method == "POST":

        if form.is_valid():
           
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("generate_bar_chart")
            else:
                msg = 'Invalid credentials provided'
            
    

    return render(request, "accounts/login.html", {"form": form, "msg": msg})



