# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    path('home', views.index, name='home'),
    path('', views.generate_bar_chart, name='generate_bar_chart'),
    path('profile_pic', views.profile_pic, name='profile_image'),
    path('supervisor', views.AddSupervisor, name='supervisor'),
    path('institute', views.AddInstitute, name='institute'),
    path('user', views.AddUser, name='user'),
    path('UserProfile', views.UserProfile, name='UserProfile'),
    path('Procedure', views.Procedure, name='Procedure'),
    path('download_pdf_file', views.download_pdf_file, name='download_pdf_file')
]

