from django.urls import path
from . import views

app_name = 'AccountApp'
urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('verify_code', views.VerifyOTP.as_view(), name='verify_code'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('forget', views.Forget.as_view(), name='forget'),
    path('forget_otp', views.ForgetOTPVerify.as_view(), name='forget_otp'),
    path('reset_password', views.ResetPassword.as_view(), name='reset_password'),
    path('enter_otp', views.EnterOTP.as_view(), name='enter_otp'),
    path('enter_otp_verify', views.EnterOTPVerify.as_view(), name='enter_otp_verify'),
    path('resend_otp', views.ResendOTP.as_view(), name='resend_otp'),
]