_H='model_list'
_G='template'
_F='template owner'
_E='abcdefghkmnprwxy2345678'
_D='email'
_C='name'
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
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django_cryptography.fields import encrypt
from menu.models import Menu
from multiselectfield import MultiSelectField
from parler.models import TranslatableModel,TranslatedFields
from region.models import Country,Province,Regency,SubDistrict,UrbanVillage
from shortuuid.django_fields import ShortUUIDField
from .abstract import BaseAbstractModel
from .managers import UserManager
class OptBillingType(models.IntegerChoices):TRANSACTION_BASE=1,_('Transaction Base');TIME_BASE=2,_('Time Base');ADVERTISE_BASE=3,_('Advertise Base')
class OptServiceType(models.IntegerChoices):ECOMMERCE=1,_('E-Commerce');AGENCY=2,_('Agency');SAAS=3,_('Saas');BUSINESS=4,_('Business');PORTOFOLIO=5,_('Portofolio');BLOG=6,_('Blog');OTHER=9,_('Other')
class Photo(BaseAbstractModel):
	file_path=models.ImageField(blank=_A,null=_A);content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,blank=_A,null=_A);object_id=models.PositiveIntegerField(blank=_A,null=_A);content_object=GenericForeignKey()
	class Meta:verbose_name=_('photo');verbose_name_plural=_('photos')
	def __str__(A):
		if A.file_path:return f"{A.file_path.url}"
		return'-'
class Agency(BaseAbstractModel,TranslatableModel):
	name=models.CharField(_(_C),max_length=100);shortuuid=ShortUUIDField(length=4,max_length=10,alphabet=_E,null=_A,blank=_A,editable=_B);email=encrypt(models.EmailField(_(_D),null=_A,blank=_A));phone=encrypt(models.CharField(_('phone'),max_length=20,null=_A,blank=_A));fax=encrypt(models.CharField(_('fax'),max_length=20,null=_A,blank=_A));whatsapp=encrypt(models.CharField(_('whatsapp'),max_length=20,null=_A,blank=_A));country=models.ForeignKey(Country,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('country'));province=models.ForeignKey(Province,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('province'));regency=models.ForeignKey(Regency,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('regency'));sub_district=models.ForeignKey(SubDistrict,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('sub district'));urban_village=models.ForeignKey(UrbanVillage,null=_A,blank=_A,on_delete=models.PROTECT,verbose_name=_('urban village'));billing_type=models.SmallIntegerField(_('billing type'),choices=OptBillingType.choices,default=OptBillingType.TIME_BASE,blank=_A);conversion=models.FloatField(default=0,blank=_A,editable=_B);translations=TranslatedFields(address=encrypt(models.CharField(_('address'),max_length=255,null=_A,blank=_A)),notes=encrypt(CKEditor5Field(_('description'),null=_A,blank=_A)));is_default=models.BooleanField(default=_B)
	class Meta:verbose_name=_('agency');verbose_name_plural=_('agencies')
	def __str__(A):return A.name
class User(AbstractBaseUser,PermissionsMixin):
	uuid=models.UUIDField(unique=_A,default=uuid.uuid4,editable=_B,blank=_A,null=_A);email=models.EmailField(_('email address'),max_length=100,unique=_A);name=models.CharField(_(_C),max_length=100,blank=_A);is_active=models.BooleanField(_('active'),default=_A);is_staff=models.BooleanField(_('staff'),default=_A);is_superuser=models.BooleanField(_('super user'),default=_B);avatar=GenericRelation(Photo);agency=models.ManyToManyField(Agency);site=models.ForeignKey(Site,on_delete=models.CASCADE,default=None,blank=_A,null=_A);email_confirmed=models.BooleanField(default=_B);date_joined=models.DateTimeField(_('date joined'),auto_now_add=_A,editable=_B);last_login=models.DateTimeField(_('last login'),null=_A,blank=_A);updated_at=models.DateTimeField(auto_now=_A,editable=_B);objects=UserManager();USERNAME_FIELD=_D;EMAIL_FIELD=_D;REQUIRED_FIELDS=[]
	class Meta:verbose_name=_('user');verbose_name_plural=_('users')
	def __str__(A):return A.email
	def get_absolute_url(A):return'/users/%i/'%A.pk
class TemplateOwner(BaseAbstractModel):
	name=models.CharField(_(_C),max_length=50)
	class Meta:verbose_name=_(_F);verbose_name_plural=_('templates owner')
	def __str__(A):return A.name
class OptStatusPublish(models.IntegerChoices):DRAFT=1,_('Draft');PUBLISHED=2,_('Published')
class Template(BaseAbstractModel):
	site=models.ManyToManyField(Site,related_name='templates_site',blank=_A);name=models.CharField(_(_C),max_length=50);rel_path=models.CharField(_('relative path'),max_length=255);is_frontend=models.BooleanField(default=_A);template_owner=models.ForeignKey(TemplateOwner,verbose_name=_(_F),on_delete=models.CASCADE,blank=_A,null=_A);service_option=MultiSelectField(choices=OptServiceType.choices,max_length=255,blank=_A,null=_A);photo=GenericRelation(Photo,verbose_name=_('photo'));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.DRAFT)
	class Meta:verbose_name=_(_G);verbose_name_plural=_('templates')
	def get_sites(A):return ', '.join([A.domain for A in A.site.all()])
	def __str__(A):return A.name
class Service(BaseAbstractModel):
	site=models.OneToOneField(Site,on_delete=models.PROTECT,blank=_A,null=_A);kind=models.SmallIntegerField(choices=OptServiceType.choices);agency=models.ForeignKey(Agency,on_delete=models.PROTECT,blank=_A,null=_A,related_name='service_agencies');is_active=models.BooleanField(default=_B);is_demo=models.BooleanField(default=_A);expired_date=models.DateTimeField();is_default=models.BooleanField(default=_B)
	class Meta:verbose_name=_('service');verbose_name_plural=_('services')
	def __str__(A):
		if A.agency:return f"{A.agency.name}"
		return'-'
class OptStatusDefault(models.IntegerChoices):DEFAULT=1,_('Default');OPTIONAL=2,_('Optional')
class ModelList(BaseAbstractModel):
	name=models.CharField(_(_C),max_length=50);description=models.CharField(_('desciption'),max_length=255);templates=models.ManyToManyField(Template,through='ModelListSetting');menu=models.OneToOneField(Menu,on_delete=models.CASCADE,default=None,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusDefault.choices,default=OptStatusDefault.OPTIONAL)
	class Meta:verbose_name=_('model list');verbose_name_plural=_('models list')
	def get_templates(A):return ', '.join([A.name for A in A.templates.all()])
	def __str__(A):return A.name
class ModelListSetting(BaseAbstractModel):
	model_list=models.ForeignKey(ModelList,on_delete=models.CASCADE);template=models.ForeignKey(Template,on_delete=models.CASCADE);image_width=models.SmallIntegerField(default=0);image_height=models.SmallIntegerField(default=0)
	class Meta:verbose_name=_('model list setting');verbose_name_plural=_('model list settings');unique_together=_H,_G
	def get_image_size(A):
		if A.image_width>0 and A.image_height>0:return f"{A.image_width} x {A.image_height} px"
		return None
class MenuDefault(BaseAbstractModel):
	model_list=models.ForeignKey(ModelList,on_delete=models.CASCADE);service_option=MultiSelectField(choices=OptServiceType.choices,max_length=255,blank=_A,null=_A)
	class Meta:verbose_name=_('menu default');verbose_name_plural=_('menus default');unique_together='service_option',_H
	def __str__(A):return''
class UserLog(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);user=models.ForeignKey(User,on_delete=models.CASCADE,blank=_A,null=_A);user_agent=models.CharField(max_length=255,editable=_B);ip_address=models.CharField(max_length=40,editable=_B);is_expired=models.BooleanField(default=_B);social_media=models.CharField(max_length=20)
	class Meta:verbose_name=_('userlog');verbose_name_plural=_('userlogs')
	def __str__(A):return A.social_media
@receiver(signals.post_save,sender=User,dispatch_uid='update_user_group')
def _update_user_group(sender,instance,**D):
	A=instance;print('signal from User',A);print('group ALL',B);B=A.groups.all()
	if not B:C=Group.objects.get(id=3);A.groups.add(C);print('done')
@receiver(signals.post_save,sender=Agency)
def _update_shortuuid(sender,instance,**D):
	C=instance;A=str(C.id);B=len(A)
	if B>4:A=A[B-4:]
	else:
		while B<4:A='0'+A;B=len(A)
	A+=shortuuid.ShortUUID(alphabet=_E).random(length=4);sender.objects.filter(id=C.id).update(shortuuid=A)
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