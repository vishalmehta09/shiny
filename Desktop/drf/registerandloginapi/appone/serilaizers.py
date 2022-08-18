from dataclasses import fields
from pyexpat import model
from . models import *
from rest_framework import serializers

class UserSerializers(serializers.Serializer):
    class Meta:
        model=User
        fields=['id','username','email','password','mobile_otp']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['name','stu_class','stu_roll']