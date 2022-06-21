# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Graphs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.FileField(upload_to='csv_files')

    def __str__(self):
        return self.user.username

