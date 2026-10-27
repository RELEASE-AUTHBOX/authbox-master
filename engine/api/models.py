_R='Site Metadata'
_Q='summary_large_image'
_P='parent'
_O='active'
_N='trust_token'
_M='device_fingerprint'
_L='expires at'
_K='setting_name'
_J='Content'
_I='order'
_H='code'
_G='-created_at'
_F=False
_E='updated at'
_D='created at'
_C='site'
_B='user'
_A=True
import os
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
from django.utils import timezone
from.common import get_site_id
from django.dispatch import receiver
import secrets,string
exposed_request=None
LEN_NAME=100
LEN_TITLE=255
class OptValueType(models.IntegerChoices):TEXT=1,_('Text-Only');IMAGE=2,_('Text-Image');VIDEO=3,_('Text-Video')
class ContentTypeChoice(models.IntegerChoices):LOGO=1,_('Logo');SLIDESHOW=2,_('Slideshow');CONTENT=3,_(_J);NAVIGATION=4,_('Navigation');FOOTER=5,_('Footer');BANNER=6,_('Banner');AVATAR=7,_('Avatar');FAVICON=8,_('Favicon');PAGES=9,_('Pages');OTHER=99,_('Other')
def site_image_path(instance,filename):A=f"{get_site_id(exposed_request)}";print(_C,A);B=os.path.join('images',A);C,D=os.path.splitext(filename);E=f"{C.strip().replace(' ','_')}{D.lower()}";return f"{B}/{E}"
class Photo(models.Model):
	content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,related_name='api_photo_set');object_id=models.PositiveIntegerField();content_object=GenericForeignKey('content_type','object_id');image=models.ImageField(_('image'),upload_to=site_image_path);title=models.CharField(_('title'),max_length=LEN_TITLE,blank=_A);alt_text=models.CharField(_('alt text'),max_length=LEN_TITLE,blank=_A);created_at=models.DateTimeField(_(_D),auto_now_add=_A);updated_at=models.DateTimeField(_(_E),auto_now=_A)
	class Meta:verbose_name=_('Photo');verbose_name_plural=_('Photos');ordering=[_G]
	def __str__(A):return A.title or f"Photo {A.id}"
class UserProfile(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile',verbose_name=_(_B));email_verified=models.BooleanField(_('email verified'),default=_F,help_text=_('Indicates if the user has verified their email address'));email_verification_token=models.CharField(_('email verification token'),max_length=100,blank=_A,help_text=_('Token for email verification'));avatar=models.ForeignKey('Photo',on_delete=models.SET_NULL,null=_A,blank=_A,related_name='user_avatars',verbose_name=_('avatar'),help_text=_('User profile avatar photo'));created_at=models.DateTimeField(_(_D),auto_now_add=_A);updated_at=models.DateTimeField(_(_E),auto_now=_A)
	class Meta:verbose_name=_('User Profile');verbose_name_plural=_('User Profiles')
	def __str__(A):return f"Profile for {A.user.username}"
	def generate_verification_token(A):A.email_verification_token=secrets.token_urlsafe(32);A.save();return A.email_verification_token
class UserSettings(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='settings',verbose_name=_(_B));site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_C));setting_name=models.CharField(_('setting name'),max_length=100,help_text=_('Name of the setting (e.g., "show_hero", "hero_text_alignment")'));setting_value=models.TextField(_('setting value'),help_text=_('Value of the setting (stored as string or JSON)'));created_at=models.DateTimeField(_(_D),auto_now_add=_A);updated_at=models.DateTimeField(_(_E),auto_now=_A)
	class Meta:verbose_name=_('User Setting');verbose_name_plural=_('User Settings');unique_together=[_B,_C,_K];indexes=[models.Index(fields=[_B,_C,_K])]
	def __str__(A):return f"{A.user.username} - {A.setting_name}: {A.setting_value}"
	@classmethod
	def get_setting(A,user,site,setting_name,default=None):
		try:B=A.objects.get(user=user,site=site,setting_name=setting_name);return B.setting_value
		except A.DoesNotExist:return default
	@classmethod
	def set_setting(A,user,site,setting_name,setting_value):B,C=A.objects.update_or_create(user=user,site=site,setting_name=setting_name,defaults={'setting_value':str(setting_value)});return B
	@classmethod
	def get_all_settings(A,user,site):B=A.objects.filter(user=user,site=site);return{A.setting_name:A.setting_value for A in B}
	@classmethod
	def set_multiple_settings(B,user,site,settings_dict):
		A=[]
		for(C,D)in settings_dict.items():E=B.set_setting(user,site,C,D);A.append(E)
		return A
	@classmethod
	def get_default_settings(A):return{'show_hero':'true','show_external_content':'false','breaking_news_animation':'default','hero_text_alignment':'center','hero_button_label':'Get Started','custom_favicon_url':''}
class OTPPurpose(models.TextChoices):LOGIN='LOGIN',_('Login');PASSWORD_RESET='PASSWORD_RESET',_('Password Reset')
class OTP(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='otps',verbose_name=_(_B));code=models.CharField(_('OTP code'),max_length=6,help_text=_('6-digit OTP code'));purpose=models.CharField(_('purpose'),max_length=20,choices=OTPPurpose.choices,default=OTPPurpose.LOGIN);is_used=models.BooleanField(_('is used'),default=_F,help_text=_('Whether this OTP has been used'));created_at=models.DateTimeField(_(_D),auto_now_add=_A);expires_at=models.DateTimeField(_(_L))
	class Meta:verbose_name=_('OTP');verbose_name_plural=_('OTPs');ordering=[_G];indexes=[models.Index(fields=[_B,_H,'is_used'])]
	def __str__(A):return f"OTP for {A.user.username} - {A.purpose}"
	def is_valid(A):return not A.is_used and timezone.now()<A.expires_at
	@classmethod
	def generate_code(A):return''.join(secrets.choice(string.digits)for A in range(6))
	@classmethod
	def create_otp(A,user,purpose=OTPPurpose.LOGIN,expiration_minutes=10):B=purpose;from django.conf import settings as C;A.objects.filter(user=user,purpose=B,is_used=_F).update(is_used=_A);D=A.generate_code();E=timezone.now()+timezone.timedelta(minutes=getattr(C,'OTP_EXPIRATION_MINUTES',expiration_minutes));return A.objects.create(user=user,code=D,purpose=B,expires_at=E)
class TrustedDevice(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='trusted_devices',verbose_name=_(_B));device_fingerprint=models.CharField(_('device fingerprint'),max_length=255,help_text=_('Unique device identifier (IP + User Agent hash)'));trust_token=models.CharField(_('trust token'),max_length=64,unique=_A,help_text=_('Token to identify this trusted device'));created_at=models.DateTimeField(_(_D),auto_now_add=_A);expires_at=models.DateTimeField(_(_L));last_used_at=models.DateTimeField(_('last used at'),auto_now=_A)
	class Meta:verbose_name=_('Trusted Device');verbose_name_plural=_('Trusted Devices');unique_together=[_B,_M];indexes=[models.Index(fields=[_B,_M]),models.Index(fields=[_N])]
	def __str__(A):return f"Trusted device for {A.user.username}"
	def is_valid(A):return timezone.now()<A.expires_at
	@classmethod
	def create_trust(A,user,device_fingerprint,days=7):B=secrets.token_urlsafe(48);C=timezone.now()+timezone.timedelta(days=days);D,E=A.objects.update_or_create(user=user,device_fingerprint=device_fingerprint,defaults={_N:B,'expires_at':C});return D
class Template(models.Model):
	name=models.CharField(_('template name'),max_length=LEN_NAME,unique=_A,help_text=_('Unique template name'));description=models.TextField(_('description'),blank=_A,help_text=_('Template description'));is_active=models.BooleanField(_(_O),default=_A);created_at=models.DateTimeField(_(_D),auto_now_add=_A);updated_at=models.DateTimeField(_(_E),auto_now=_A)
	class Meta:verbose_name=_('Template');verbose_name_plural=_('Templates');ordering=['name']
	def __str__(A):return A.name
class Content(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_C));code=models.CharField(_(_H),max_length=LEN_NAME,help_text=_('Code for AJAX identification'));slug=models.SlugField(_('slug'),max_length=LEN_TITLE,blank=_A,help_text=_('SEO-friendly URL slug (auto-generated from title)'));url=models.CharField(_('url'),max_length=500,blank=_A,null=_A,help_text=_('Custom URL for navigation menu items'));value_type=models.SmallIntegerField(choices=OptValueType.choices,verbose_name=_('value type'));content_type=models.SmallIntegerField(choices=ContentTypeChoice.choices,default=ContentTypeChoice.OTHER,verbose_name=_('content type'),help_text=_('Type of content (logo, slideshow, content, etc.)'));is_page=models.BooleanField(_('is page'),default=_F,help_text=_('Mark this content as a page (vs regular content/article)'));value_text=models.CharField(_('text'),max_length=LEN_TITLE,null=_A,blank=_A);value_image=GenericRelation(Photo,related_query_name='content');value_textarea=CKEditor5Field(_('value textarea'),blank=_A,null=_A,config_name='extends');value_video=models.URLField(_('video URL'),max_length=500,blank=_A,null=_A,help_text=_('Video URL (YouTube, Vimeo, or direct video link)'));template=models.ForeignKey(Template,on_delete=models.SET_NULL,null=_A,blank=_A,related_name='contents',verbose_name=_('template'),help_text=_('Template reference'));parent=models.ForeignKey('self',on_delete=models.CASCADE,null=_A,blank=_A,related_name='children',verbose_name=_(_P));order=models.IntegerField(_(_I),default=0);is_active=models.BooleanField(_(_O),default=_A);created_at=models.DateTimeField(_(_D),auto_now_add=_A);updated_at=models.DateTimeField(_(_E),auto_now=_A)
	class Meta:verbose_name=_(_J);verbose_name_plural=_('Contents');ordering=[_I,_G];indexes=[models.Index(fields=[_C,_H]),models.Index(fields=[_C,'slug']),models.Index(fields=[_P]),models.Index(fields=['value_type'])]
	def __str__(A):return f"{A.code} - {A.get_value_type_display()}"
	def get_children(A):return A.children.filter(is_active=_A)
	def get_all_descendants(C):
		A=[]
		for B in C.get_children():A.append(B);A.extend(B.get_all_descendants())
		return A
	def save(A,*E,**F):
		if not A.slug and A.value_text:
			from django.utils.text import slugify as G;C=G(A.value_text);B=C;D=1
			while Content.objects.filter(site=A.site,slug=B).exclude(pk=A.pk).exists():B=f"{C}-{D}";D+=1
			A.slug=B
		if A.order==0:H=Content.objects.filter(site=A.site,parent=A.parent).aggregate(models.Max(_I))['order__max']or 0;A.order=H+1
		super().save(*E,**F)
class SiteMetadata(models.Model):
	site=models.OneToOneField(Site,on_delete=models.CASCADE,related_name='metadata',verbose_name=_(_C));site_title=models.CharField(_('site title'),max_length=LEN_TITLE,help_text=_('Main website title (shown in browser tab)'));site_tagline=models.CharField(_('site tagline'),max_length=LEN_TITLE,blank=_A,help_text=_('Short tagline or slogan'));meta_description=models.TextField(_('meta description'),max_length=160,help_text=_('SEO meta description (recommended: 150-160 characters)'));meta_keywords=models.CharField(_('meta keywords'),max_length=LEN_TITLE,blank=_A,help_text=_('Comma-separated keywords for SEO'));og_title=models.CharField(_('og:title'),max_length=LEN_TITLE,blank=_A,help_text=_('Open Graph title (if different from site title)'));og_description=models.TextField(_('og:description'),max_length=200,blank=_A,help_text=_('Open Graph description'));og_image=models.ImageField(_('og:image'),upload_to='og_images/%Y/%m/%d/',blank=_A,null=_A,help_text=_('Open Graph image (recommended: 1200x630px)'));og_type=models.CharField(_('og:type'),max_length=50,default='website',help_text=_('Open Graph type (website, article, etc.)'));twitter_card=models.CharField(_('twitter:card'),max_length=50,default=_Q,choices=[('summary','Summary'),(_Q,'Summary Large Image'),('app','App'),('player','Player')],help_text=_('Twitter card type'));twitter_site=models.CharField(_('twitter:site'),max_length=100,blank=_A,help_text=_('Twitter handle of website (e.g., @username)'));twitter_creator=models.CharField(_('twitter:creator'),max_length=100,blank=_A,help_text=_('Twitter handle of content creator'));favicon=models.ImageField(_('favicon'),upload_to='favicons/',blank=_A,null=_A,help_text=_('Website favicon (.ico or .png, recommended: 32x32px)'));apple_touch_icon=models.ImageField(_('apple touch icon'),upload_to='icons/',blank=_A,null=_A,help_text=_('Apple touch icon (recommended: 180x180px)'));logo=models.ImageField(_('logo'),upload_to='logos/',blank=_A,null=_A,help_text=_('Website logo'));theme_color=models.CharField(_('theme color'),max_length=7,default='#ffffff',help_text=_('Theme color for mobile browsers (hex color code)'));canonical_url=models.URLField(_('canonical URL'),blank=_A,help_text=_('Canonical URL for the site'));robots=models.CharField(_('robots'),max_length=100,default='index, follow',help_text=_('Robots meta tag content'));google_site_verification=models.CharField(_('google site verification'),max_length=100,blank=_A,help_text=_('Google Search Console verification code'));google_analytics_id=models.CharField(_('google analytics ID'),max_length=50,blank=_A,help_text=_('Google Analytics tracking ID (e.g., G-XXXXXXXXXX)'));facebook_app_id=models.CharField(_('facebook app ID'),max_length=50,blank=_A,help_text=_('Facebook App ID'));created_at=models.DateTimeField(_(_D),auto_now_add=_A);updated_at=models.DateTimeField(_(_E),auto_now=_A)
	class Meta:verbose_name=_(_R);verbose_name_plural=_(_R)
	def __str__(A):return f"Metadata for {A.site.domain}"
	def get_og_title(A):return A.og_title or A.site_title
	def get_og_description(A):return A.og_description or A.meta_description
	def get_og_image_url(A):
		if A.og_image:return A.og_image.url
@receiver(models.signals.post_delete,sender=Photo)
def auto_delete_file_on_delete(sender,instance,**B):
	A=instance
	if A.image:
		if os.path.isfile(A.image.path):os.remove(A.image.path)
@receiver(models.signals.pre_save,sender=Photo)
def auto_delete_file_on_change(sender,instance,**E):
	C=sender;A=instance
	if not A.pk:return _F
	try:B=C.objects.get(pk=A.pk).image
	except C.DoesNotExist:return _F
	D=A.image
	if not B==D:
		if os.path.isfile(B.path):os.remove(B.path)