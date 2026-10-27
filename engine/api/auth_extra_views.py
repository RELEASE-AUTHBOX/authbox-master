_H='dispatch'
_G='Password must be at least 8 characters long'
_F='Passwords do not match'
_E='password_confirm'
_D=False
_C='message'
_B='email'
_A='error'
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import re
from.models import UserProfile,OTP,OTPPurpose
User=get_user_model()
@method_decorator(ratelimit(key='ip',rate='3/hour',method='POST'),name=_H)
class RegisterView(APIView):
	permission_classes=[AllowAny]
	def post(E,request):
		D=request;A=D.data.get(_B);C=D.data.get('password');F=D.data.get(_E)
		if not all([A,C,F]):return Response({_A:'Email, password, and password confirmation are required'},status=status.HTTP_400_BAD_REQUEST)
		if not E._is_valid_email(A):return Response({_A:'Invalid email format'},status=status.HTTP_400_BAD_REQUEST)
		if C!=F:return Response({_A:_F},status=status.HTTP_400_BAD_REQUEST)
		if len(C)<8:return Response({_A:_G},status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(email=A).exists():return Response({_A:'An account with this email already exists'},status=status.HTTP_400_BAD_REQUEST)
		B=A.split('@')[0];I=B;G=1
		while User.objects.filter(username=B).exists():B=f"{I}{G}";G+=1
		H=User.objects.create_user(username=B,email=A,password=C);J=UserProfile.objects.create(user=H);K=J.generate_verification_token();E._send_verification_email(H,K);return Response({_C:'Registration successful! Please check your email to verify your account.',_B:A,'username':B},status=status.HTTP_201_CREATED)
	def _is_valid_email(B,email):A='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$';return re.match(A,email)is not None
	def _send_verification_email(D,user,token):A=f"{settings.FRONTEND_URL}/verify-email/{token}";B='Verify Your Email Address';C=f"""
Hello {user.username},
Thank you for registering! Please verify your email address by clicking the link below:
{A}
This link will expire in 24 hours.
If you didn't create this account, please ignore this email.
Best regards,
Your Application Team
        """;send_mail(subject=B,message=C,from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[user.email],fail_silently=_D)
@method_decorator(ratelimit(key='ip',rate='3/15m',method='POST'),name=_H)
class ForgotPasswordView(APIView):
	permission_classes=[AllowAny]
	def post(D,request):
		C='If an account with this email exists, a password reset code has been sent.';A=request.data.get(_B)
		if not A:return Response({_A:'Email is required'},status=status.HTTP_400_BAD_REQUEST)
		try:B=User.objects.get(email=A)
		except User.DoesNotExist:return Response({_C:C},status=status.HTTP_200_OK)
		E=OTP.create_otp(B,purpose=OTPPurpose.PASSWORD_RESET);D._send_reset_email(B,E.code);return Response({_C:C,_B:A},status=status.HTTP_200_OK)
	def _send_reset_email(C,user,otp_code):A='Password Reset Code';B=f"""
Hello {user.username},
Your password reset code is: {otp_code}
This code will expire in {settings.OTP_EXPIRATION_MINUTES} minutes.
If you didn't request a password reset, please ignore this email and ensure your account is secure.
Best regards,
Your Application Team
        """;send_mail(subject=A,message=B,from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[user.email],fail_silently=_D)
class ResetPasswordView(APIView):
	permission_classes=[AllowAny]
	def post(H,request):
		A=request;E=A.data.get(_B);F=A.data.get('otp');B=A.data.get('new_password');G=A.data.get(_E)
		if not all([E,F,B,G]):return Response({_A:'Email, OTP code, and new password are required'},status=status.HTTP_400_BAD_REQUEST)
		if B!=G:return Response({_A:_F},status=status.HTTP_400_BAD_REQUEST)
		if len(B)<8:return Response({_A:_G},status=status.HTTP_400_BAD_REQUEST)
		try:D=User.objects.get(email=E)
		except User.DoesNotExist:return Response({_A:'Invalid email or OTP code'},status=status.HTTP_400_BAD_REQUEST)
		C=OTP.objects.filter(user=D,code=F,purpose=OTPPurpose.PASSWORD_RESET,is_used=_D).first()
		if not C:return Response({_A:'Invalid OTP code'},status=status.HTTP_400_BAD_REQUEST)
		if not C.is_valid():return Response({_A:'OTP code has expired. Please request a new one.'},status=status.HTTP_400_BAD_REQUEST)
		C.is_used=True;C.save();D.set_password(B);D.save();return Response({_C:'Password reset successful! You can now login with your new password.'},status=status.HTTP_200_OK)