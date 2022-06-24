# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Graphs)
admin.site.register(Institution)
admin.site.register(NormalUser)

