from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Student(models.Model):
    name=models.CharField(max_length=100)
    stu_class=models.CharField(max_length=40)
    stu_roll=models.CharField(max_length=50,null=True,blank=True)


class CustomUser(AbstractUser):
    mobile_otp = models.CharField(max_length=200, blank=True)
    mobile_no=models.CharField(max_length=50 ,blank=False)
    counter = models.IntegerField(default=0, blank=False)
