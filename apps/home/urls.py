# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    path('home', views.index, name='home'),
    path('', views.generate_bar_chart, name='generate_bar_chart'),
    path("change_password", views.change_password, name='change_password')

]

