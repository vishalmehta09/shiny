from .import views
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/',views.register),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/]',views.activate,name="activate"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify_otp/',views.myotp),
    path('forgot_password/',views.forgot_password),
    path('change_password/',views.change_password),
    path('student',views.ExampleView.as_view())
]

   