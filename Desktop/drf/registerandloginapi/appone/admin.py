from django.contrib import admin
from .models import *
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name','stu_class','stu_roll']
admin.site.register(Student,StudentAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'email', 'password', 'mobile_otp'
    ]

admin.site.register(CustomUser, CustomUserAdmin)