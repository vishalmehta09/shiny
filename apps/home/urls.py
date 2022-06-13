# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('generate_bar_chart', views.generate_bar_chart, name='generate_bar_chart'),


    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]

