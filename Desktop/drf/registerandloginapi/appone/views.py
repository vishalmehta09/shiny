
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseGone,response
from rest_framework.response import Response
from .models import  *
from rest_framework import status
import random
import math
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site  
# from rest_framework.decorators import api_view
from appone.serilaizers import *
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth.tokens import default_token_generator 
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
import base64
from appone.helpers import send_otp
from django.contrib.auth.hashers import make_password


@api_view(['POST'])
def register(request):
    usr=""
    serializer=UserSerializers(data=request.data)
    get_mobile_no=request.data['mobile_no']
    User = get_user_model()
    otp=random.randint(1000,9999)
    if serializer.is_valid():
        obj=User.objects.create(username=request.data['username'],email=request.data['email'],mobile_no=(request.data['mobile_no']),mobile_otp=otp)
        obj.set_password(request.data['password'])
        obj.is_active=False
        obj.save()
        current_site = get_current_site(request) 
        usr = User.objects.get(username=request.data['username'])
        usr_id=usr.id 
        mail_subject = 'Activation link has been sent to your email id'  
        message = render_to_string('index.html', {  
                'user': obj,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(usr_id)),  
                'token':default_token_generator.make_token(obj),  
            }) 
        get_email_id=request.data['mobile_no'] 
        email_get=[]
        email_get.append(get_email_id)
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject,message,from_email,email_get)
        send_otp(get_mobile_no,otp)
        return HttpResponse('Please confirm your email address to complete the registration')  
    else:  
        return render(request,"index.html")

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and default_token_generator.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return Response({"success":"Thank you for your email confirmation. Now you can login your account."})  
    else:  
        return HttpResponse('Activation link is invalid!')  


class ExampleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer=StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Activation link is invalid!"})  
    
@api_view(['POST'])
def myotp(request):
    User=get_user_model
    get_user=request.data['username']
    get_user_id=CustomUser.objects.get(username=get_user)
    get_mobile_otp=get_user_id.mobile_otp
    get_otp_by_pstmn=request.data['mobile_otp']
    if get_mobile_otp==get_otp_by_pstmn:
        get_user_id.mobile_otp=""
        get_user_id.save()
        return Response({"success":"Matched"})
    if get_otp_by_pstmn!=get_mobile_otp:
        return HttpResponse({"error":"Not Matched"})

@api_view(['POST'])
def forgot_password(request):
    
    get_user_name=request.data['username']
    get_mobile_no=CustomUser.objects.filter(username=get_user_name).values('mobile_no','email')
    get_mobile_no_of_user=get_mobile_no[0]['mobile_no']
    get_email_id= get_mobile_no[0]['email']
    if CustomUser.objects.filter(email = get_email_id).first():
        otp=random.randint(1000,9999)
        send_otp(get_mobile_no_of_user,otp)
        message = str(otp)
        email_get = []
        email_get.append(get_email_id)
        from_email = settings.EMAIL_HOST_USER
        send_mail('Your OTP is',message,from_email,email_get)
        obj=CustomUser.objects.get(username=get_user_name)
        obj.mobile_otp=otp
        obj.save()
    return Response({'status':"success"},status=status.HTTP_200_OK)

@api_view(['POST'])
def change_password(request):
   get_new_password=request.data['newpassword']
   get_confirm_password=request.data['confirmpassword']
   get_user_otp=request.data['mobile_otp']  
   try:
        get_userotp = CustomUser.objects.get(mobile_otp=request.data['mobile_otp'])
        if get_userotp:
            get_usrrname=get_userotp.username
            if get_new_password==get_confirm_password:
                get_userotp.password=make_password(get_confirm_password)
                get_userotp.is_active=True
                get_userotp.save()
            if get_new_password!=get_confirm_password:
                return Response({"error": "Password doesnot Match"})
                
   except Exception as e :
        return Response({"error":"Invalid OTP"})
        
   return Response({"status": "success"}, status=status.HTTP_200_OK)