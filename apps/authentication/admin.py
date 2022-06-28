from django.contrib import admin
from django.utils.translation import gettext as _
from django.contrib.auth.admin import UserAdmin
from apps.authentication.models import *
from django import forms
from django.forms import ModelForm, PasswordInput


class UserCreationForm(forms.ModelForm):
    
    class Meta:
        model = NewUser
        fields = ('username',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

   

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("username",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ("username",'email', 'password', 'first_name', 'last_name','is_active','institute','normal_user')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','first_name','last_name','password','password1', 'institute','normal_user','is_active')}
            ),
        )
    

    filter_horizontal = ()

admin.site.register(NewUser, CustomUserAdmin)

