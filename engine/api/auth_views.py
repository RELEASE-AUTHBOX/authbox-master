_K='Invalid username'
_J='dispatch'
_I='Login successful'
_H='django.contrib.auth.backends.ModelBackend'
_G='email_verified'
_F='email'
_E='user'
_D=True
_C='message'
_B='username'
_A='error'
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from captcha.models import CaptchaStore
from django.utils import timezone
from.models import UserProfile,OTP,OTPPurpose,TrustedDevice
User=get_user_model()
def get_device_fingerprint(request):A=request;import hashlib as B;C=A.META.get('REMOTE_ADDR','');D=A.META.get('HTTP_USER_AGENT','');E=f"{C}:{D}";return B.sha256(E.encode()).hexdigest()
@method_decorator(ratelimit(key='ip',rate='50/15m',method='POST'),name=_J)
class LoginView(APIView):
	permission_classes=[AllowAny]
	def post(I,request):
		A=request;D=A.data.get(_B);E=A.data.get('password');F=A.data.get('captchaKey');G=A.data.get('captchaValue')
		if not all([D,E,F,G]):return Response({_A:'Username, password, and captcha are required'},status=status.HTTP_400_BAD_REQUEST)
		try:
			C=CaptchaStore.objects.get(hashkey=F)
			if C.expiration<timezone.now():C.delete();return Response({_A:'Captcha has expired. Please refresh and try again.'},status=status.HTTP_400_BAD_REQUEST)
			if C.response.lower()!=G.lower():return Response({_A:'Invalid captcha. Please try again.'},status=status.HTTP_400_BAD_REQUEST)
			C.delete()
		except CaptchaStore.DoesNotExist:return Response({_A:'Invalid captcha. Please refresh and try again.'},status=status.HTTP_400_BAD_REQUEST)
		B=authenticate(username=D,password=E)
		if not B:return Response({_A:'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)
		login(A,B,backend=_H);H,J=UserProfile.objects.get_or_create(user=B);return Response({'skip_otp':_D,_C:_I,_E:{'id':B.id,_F:B.email,_G:H.email_verified}},status=status.HTTP_200_OK)
class CaptchaRefreshView(APIView):
	permission_classes=[AllowAny]
	def get(D,request):
		from captcha.helpers import captcha_image_url as C;from captcha.models import CaptchaStore as B;E=B.generate_key();A=B.objects.order_by('-id').first()
		if A:return Response({'key':A.hashkey,'image_url':C(A.hashkey)},status=status.HTTP_200_OK)
		else:return Response({_A:'Failed to generate captcha'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class VerifyOTPView(APIView):
	permission_classes=[AllowAny]
	def post(K,request):
		B=request;D=B.data.get(_B);E=B.data.get('otp');G=B.data.get('remember_device',_D)
		if not all([D,E]):return Response({_A:'Username and OTP code are required'},status=status.HTTP_400_BAD_REQUEST)
		try:A=User.objects.get(username=D)
		except User.DoesNotExist:return Response({_A:_K},status=status.HTTP_404_NOT_FOUND)
		C=OTP.objects.filter(user=A,code=E,purpose=OTPPurpose.LOGIN,is_used=False).first()
		if not C:return Response({_A:'Invalid OTP code'},status=status.HTTP_400_BAD_REQUEST)
		if not C.is_valid():return Response({_A:'OTP code has expired. Please request a new one.'},status=status.HTTP_400_BAD_REQUEST)
		C.is_used=_D;C.save();login(B,A,backend=_H);F=None
		if G:H=get_device_fingerprint(B);I=TrustedDevice.create_trust(A,H,days=7);F=I.trust_token
		J=UserProfile.objects.get(user=A);return Response({_C:_I,'trust_token':F,_E:{'id':A.id,_B:A.username,_F:A.email,_G:J.email_verified}},status=status.HTTP_200_OK)
@method_decorator(ratelimit(key='ip',rate='3/15m',method='POST'),name=_J)
class ResendOTPView(APIView):
	permission_classes=[AllowAny]
	def post(C,request):
		A=request.data.get(_B)
		if not A:return Response({_A:'Username is required'},status=status.HTTP_400_BAD_REQUEST)
		try:B=User.objects.get(username=A)
		except User.DoesNotExist:return Response({_A:_K},status=status.HTTP_404_NOT_FOUND)
		D=OTP.create_otp(B,purpose=OTPPurpose.LOGIN);C._send_otp_email(B,D.code);return Response({_C:'New OTP sent to your email'},status=status.HTTP_200_OK)
	def _send_otp_email(F,user,otp_code):
		C=otp_code;A=user;E='Your Login OTP Code (Resent)'
		try:B=render_to_string('otp_email.html',{_E:A,'otp_code':C,'expiration_minutes':settings.OTP_EXPIRATION_MINUTES});D=strip_tags(B)
		except:D=f"""
Hello {A.username},
Your NEW OTP code for login is: {C}
This code will expire in {settings.OTP_EXPIRATION_MINUTES} minutes.
If you didn't request this code, please ignore this email.
Best regards,
Your Application Team
            """;B=None
		send_mail(subject=E,message=D,from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[A.email],html_message=B,fail_silently=False)
class CurrentUserView(APIView):
	permission_classes=[IsAuthenticated]
	def get(C,request):A=request.user;B,D=UserProfile.objects.get_or_create(user=A);return Response({'id':A.id,_B:A.username,_F:A.email,_G:B.email_verified},status=status.HTTP_200_OK)
class LogoutView(APIView):
	permission_classes=[AllowAny];authentication_classes=[]
	def post(A,request):logout(request);return Response({_C:'Logout successful'},status=status.HTTP_200_OK)
class VerifyEmailView(APIView):
	permission_classes=[AllowAny]
	def get(C,request,token):
		try:
			A=UserProfile.objects.get(email_verification_token=token)
			if not A.email_verified:A.email_verified=_D;A.save();B='Email verified successfully!'
			else:B='Email already verified.'
			return Response({_C:B},status=status.HTTP_200_OK)
		except UserProfile.DoesNotExist:return Response({_A:'Invalid verification token'},status=status.HTTP_400_BAD_REQUEST)