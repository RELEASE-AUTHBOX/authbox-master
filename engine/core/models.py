_K='model_list'
_J='template'
_I='template owner'
_H='description'
_G='abcdefghkmnprwxy2345678'
_F='email'
_E='photo'
_D='name'
_C=None
_B=False
_A=True
import os,uuid
from django.contrib.auth.models import Group
import shortuuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django_cryptography.fields import encrypt
from menu.models import Menu
from multiselectfield import MultiSelectField
from parler.models import TranslatableModel,TranslatedFields
from region.models import Country,Province,Regency,SubDistrict,UrbanVillage
from shortuuid.django_fields import ShortUUIDField
from.managers import UserManager
from.abstract import BaseAbstractModel
from django.db.models import Max
exposed_request=_C
def get_site_id(request):
	D=request
	if not D:return-1
	E=D.user.id
	if not E:return-1
	C=User.objects.filter(id=D.user.id)
	if not C:return-2
	C=C.get();A=C.agency.filter(is_default=_A)
	if not A:return-3
	if len(A)>1:return-31
	A=A[0];print('agency == ',A);B=Service.objects.filter(agency_id=A.id,is_default=_A)
	if not B:return-4
	if len(B)>1:return-41
	B=B[0]
	if B:return B.site_id
	return 0
class OptBillingType(models.IntegerChoices):TRANSACTION_BASE=1,_('Transaction Base');TIME_BASE=2,_('Time Base');ADVERTISE_BASE=3,_('Advertise Base')
class OptServiceType(models.IntegerChoices):ECOMMERCE=1,_('E-Commerce');AGENCY=2,_('Agency');SAAS=3,_('Saas');BUSINESS=4,_('Business');PORTOFOLIO=5,_('Portofolio');BLOG=6,_('Blog');EDUCATION=7,_('Education');OTHER=9,_('Other')
class OptColorTheme(models.IntegerChoices):SLATE=81,_('slate');GRAY=73,_('gray');ZINC=72,_('zinc');NEUTRAL=71,_('neutral');STONE=63,_('stone');RED=62,_('red');ORANGE=61,_('orange');AMBER=53,_('amber');YELLOW=52,_('yellow');LIME=51,_('lime');GREEN=43,_('green');EMERALD=42,_('emerald');TEAL=41,_('teal');CYAN=33,_('cyan');SKY=32,_('sky');BLUE=31,_('blue');INDIGO=23,_('indigo');VIOLET=22,_('violet');PURPLE=21,_('purple');FUCHSIA=13,_('fuchsia');PINK=12,_('pink');ROSE=11,_('rose')
class Photo(BaseAbstractModel):
	file_path=models.ImageField(blank=_A,null=_A,upload_to='temp');content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,blank=_A,null=_A);object_id=models.PositiveIntegerField(blank=_A,null=_A);content_object=GenericForeignKey()
	class Meta:verbose_name=_(_E);verbose_name_plural=_('photos')
	def __str__(A):
		if A.file_path:return f"{A.file_path.url}"
		return'-'
class Agency(BaseAbstractModel,TranslatableModel):
	name=models.CharField(_(_D),max_length=100);shortuuid=ShortUUIDField(length=4,max_length=10,alphabet=_G,null=_A,blank=_A,editable=_B);email=encrypt(models.EmailField(_(_F),null=_A,blank=_A));phone=encrypt(models.CharField(_('phone'),max_length=20,null=_A,blank=_A));fax=encrypt(models.CharField(_('fax'),max_length=20,null=_A,blank=_A));whatsapp=encrypt(models.CharField(_('whatsapp'),max_length=20,null=_A,blank=_A));country=models.ForeignKey(Country,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('country'));province=models.ForeignKey(Province,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('province'));regency=models.ForeignKey(Regency,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('regency'));sub_district=models.ForeignKey(SubDistrict,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('sub district'));urban_village=models.ForeignKey(UrbanVillage,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('urban village'));billing_type=models.SmallIntegerField(_('billing type'),choices=OptBillingType.choices,default=OptBillingType.TIME_BASE,blank=_A);conversion=models.FloatField(default=0,blank=_A,editable=_B);translations=TranslatedFields(address=encrypt(models.CharField(_('address'),max_length=255,null=_A,blank=_A)),notes=encrypt(CKEditor5Field(_(_H),null=_A,blank=_A)));is_default=models.BooleanField(default=_B)
	class Meta:verbose_name=_('agency');verbose_name_plural=_('agencies')
	def __str__(A):return A.name
class OptImageType(models.IntegerChoices):JPEG=1,'image/jpeg';PNG=2,'image/png'
class OptLocaleType(models.IntegerChoices):INDONESIA=1,'id_ID';ENGLISH=2,'en_US'
class OptWebType(models.IntegerChoices):WEBSITE=1,'website';ARTICLE=2,'article';PROFILE=3,'profile';BOOK=4,'book';VIDEO=5,'video';MOVIE=6,'movie';EDUCATION=7,'education';NEWS=8,'news'
class AgencyMeta(BaseAbstractModel):
	agency=models.OneToOneField(Agency,on_delete=models.PROTECT,blank=_A,null=_A);name=models.CharField(_('site name'),max_length=100,blank=_A,null=_A);url=models.CharField(_('URL'),max_length=255);title=models.CharField(_('title'),max_length=255);description=models.CharField(_(_H),max_length=500);web_type=models.SmallIntegerField(_('web type'),choices=OptWebType.choices,default=OptWebType.WEBSITE,blank=_A);locale=models.SmallIntegerField(_('locale'),choices=OptLocaleType.choices,default=OptLocaleType.INDONESIA,blank=_A);locale_alternate=models.SmallIntegerField(_('locale alternate'),choices=OptLocaleType.choices,default=OptLocaleType.ENGLISH,blank=_A);image=GenericRelation(Photo);image_type=models.SmallIntegerField(_('image type'),choices=OptImageType.choices,default=OptImageType.JPEG,blank=_A)
	class Meta:verbose_name=_('agency meta');verbose_name_plural=_('agency metas')
	def __str__(A):
		if A.name:return A.name
		return'-'
class User(AbstractBaseUser,PermissionsMixin):
	uuid=models.UUIDField(unique=_A,default=uuid.uuid4,editable=_B,blank=_A,null=_A);email=models.EmailField(_('email address'),max_length=100,unique=_A);name=models.CharField(_(_D),max_length=100,blank=_A);is_active=models.BooleanField(_('active'),default=_A);is_staff=models.BooleanField(_('staff'),default=_A);is_superuser=models.BooleanField(_('super user'),default=_B);avatar=GenericRelation(Photo);agency=models.ManyToManyField(Agency);site=models.ForeignKey(Site,on_delete=models.CASCADE,default=_C,blank=_A,null=_A);email_confirmed=models.BooleanField(default=_B);date_joined=models.DateTimeField(_('date joined'),auto_now_add=_A,editable=_B);last_login=models.DateTimeField(_('last login'),null=_A,blank=_A);updated_at=models.DateTimeField(auto_now=_A,editable=_B);objects=UserManager();USERNAME_FIELD=_F;EMAIL_FIELD=_F;REQUIRED_FIELDS=[]
	class Meta:verbose_name=_('user');verbose_name_plural=_('users')
	def __str__(A):return A.email
	def get_absolute_url(A):return'/users/%i/'%A.pk
class TemplateOwner(BaseAbstractModel):
	name=models.CharField(_(_D),max_length=50)
	class Meta:verbose_name=_(_I);verbose_name_plural=_('templates owner')
	def __str__(A):return A.name
class OptStatusPublish(models.IntegerChoices):DRAFT=1,_('Draft');PUBLISHED=2,_('Published')
class OptPriceLevel(models.IntegerChoices):LEVEL_1=1,_('Level 1');LEVEL_2=2,_('Level 2');LEVEL_3=3,_('Level 3');LEVEL_9=9,_('Custom Level')
class OptSettingName(models.IntegerChoices):SLIDE_SHOW=1,_('Slide Show');MENU=2,_('Menu');WHY_US=3,_('Why Us')
class Template(BaseAbstractModel):
	site=models.ManyToManyField(Site,related_name='templates_site',blank=_A);name=models.CharField(_(_D),max_length=50);rel_path=models.CharField(_('relative path'),max_length=255);is_frontend=models.BooleanField(default=_A);template_owner=models.ForeignKey(TemplateOwner,verbose_name=_(_I),on_delete=models.CASCADE,blank=_A,null=_A);service_option=MultiSelectField(choices=OptServiceType.choices,max_length=255,blank=_A,null=_A);photo=GenericRelation(Photo,verbose_name=_(_E));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.DRAFT)
	class Meta:verbose_name=_(_J);verbose_name_plural=_('templates')
	def get_sites(A):return', '.join([A.domain for A in A.site.all()])
	def __str__(A):return A.name
class IconList(BaseAbstractModel):
	template=models.ForeignKey(Template,on_delete=models.CASCADE);icon=models.CharField(_('icon'),max_length=100,null=_A,blank=_A)
	def __str__(A):return f"{A.icon}"
class Service(BaseAbstractModel):
	site=models.OneToOneField(Site,on_delete=models.PROTECT,blank=_A,null=_A);kind=models.SmallIntegerField(choices=OptServiceType.choices);agency=models.ForeignKey(Agency,on_delete=models.PROTECT,blank=_A,null=_A,related_name='service_agencies');is_active=models.BooleanField(default=_B);is_demo=models.BooleanField(default=_A);expired_date=models.DateTimeField();is_default=models.BooleanField(default=_B)
	class Meta:verbose_name=_('service');verbose_name_plural=_('services')
	def __str__(A):
		if A.agency:return f"{A.agency.name}"
		return'-'
class OptStatusDefault(models.IntegerChoices):DEFAULT=1,_('Default');OPTIONAL=2,_('Optional')
class ModelList(BaseAbstractModel):
	name=models.CharField(_(_D),max_length=50);description=models.CharField(_('desciption'),max_length=255);templates=models.ManyToManyField(Template,through='ModelListSetting');menu=models.OneToOneField(Menu,on_delete=models.CASCADE,default=_C,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusDefault.choices,default=OptStatusDefault.OPTIONAL)
	class Meta:verbose_name=_('model list');verbose_name_plural=_('models list')
	def get_templates(A):return', '.join([A.name for A in A.templates.all()])
	def __str__(A):return A.name
class ModelListSetting(BaseAbstractModel):
	model_list=models.ForeignKey(ModelList,on_delete=models.CASCADE);template=models.ForeignKey(Template,on_delete=models.CASCADE);image_width=models.SmallIntegerField(default=0);image_height=models.SmallIntegerField(default=0)
	class Meta:verbose_name=_('model list setting');verbose_name_plural=_('model list settings');unique_together=_K,_J
	def get_image_size(A):
		if A.image_width>0 and A.image_height>0:return f"{A.image_width} x {A.image_height} px"
class MenuDefault(BaseAbstractModel):
	model_list=models.ForeignKey(ModelList,on_delete=models.CASCADE);service_option=MultiSelectField(choices=OptServiceType.choices,max_length=255,blank=_A,null=_A)
	class Meta:verbose_name=_('menu default');verbose_name_plural=_('menus default');unique_together='service_option',_K
	def __str__(A):return''
class UserLog(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);user=models.ForeignKey(User,on_delete=models.CASCADE,blank=_A,null=_A);user_agent=models.CharField(max_length=255,editable=_B);ip_address=models.CharField(max_length=40,editable=_B);is_expired=models.BooleanField(default=_B);social_media=models.CharField(max_length=20)
	class Meta:verbose_name=_('userlog');verbose_name_plural=_('userlogs')
	def __str__(A):return A.social_media
class TemplateBlock(BaseAbstractModel):
	template=models.ForeignKey(Template,on_delete=models.CASCADE,blank=_A);model_list=models.ManyToManyField(ModelList,blank=_A);name=models.CharField(_('block name'),max_length=100);photo=GenericRelation(Photo,verbose_name=_(_E));price_level=models.SmallIntegerField(choices=OptPriceLevel.choices,default=OptPriceLevel.LEVEL_1);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.DRAFT);description=models.TextField(null=_A,blank=_A)
	class Meta:verbose_name=_('template block');verbose_name_plural=_('template blocks')
	def __str__(A):return A.name
class GlobalSetting(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);name=models.SmallIntegerField(choices=OptSettingName.choices,default=_C);value=models.CharField(_('value'),max_length=255,null=_A,blank=_A,default=_C);ref_template_block=models.ForeignKey(TemplateBlock,on_delete=models.CASCADE,null=_A,default=_A);order_item=models.PositiveIntegerField(default=0)
	class Meta:verbose_name=_('global setting');verbose_name_plural=_('global settings')
	def __str__(A):
		if A.name:return A.get_name_display()
		return'-'
	def save(B,*D,**E):
		C='max'
		if B.order_item==0:
			A=GlobalSetting.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max('order_item'))
			if A:
				if not A[C]is _C:B.order_item=A[C]+1
		super().save(*D,**E)
@receiver(signals.post_save,sender=User,dispatch_uid='update_user_group')
def _update_user_group(sender,instance,**D):
	A=instance;print('signal from User',A);B=A.groups.all()
	if not B:C=Group.objects.get(id=3);A.groups.add(C);print('done')
@receiver(signals.post_save,sender=Agency)
def _update_shortuuid(sender,instance,**D):
	C=instance;A=str(C.id);B=len(A)
	if B>4:A=A[B-4:]
	else:
		while B<4:A='0'+A;B=len(A)
	A+=shortuuid.ShortUUID(alphabet=_G).random(length=4);sender.objects.filter(id=C.id).update(shortuuid=A)
@receiver(models.signals.post_delete,sender=Photo)
def auto_delete_file_on_delete(sender,instance,**B):
	A=instance
	if A.file_path:
		if os.path.isfile(A.file_path.path):os.remove(A.file_path.path)
@receiver(models.signals.pre_save,sender=Photo)
def auto_delete_file_on_change(sender,instance,**E):
	C=sender;A=instance
	if not A.pk:return _B
	try:B=C.objects.get(pk=A.pk).file_path
	except C.DoesNotExist:return _B
	D=A.file_path
	if not B==D:
		if os.path.isfile(B.path):os.remove(B.path)