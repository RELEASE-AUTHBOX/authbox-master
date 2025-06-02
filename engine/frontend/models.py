_g='menu_2'
_f='menu_1'
_e='menu_active'
_d='menu_class_2'
_c='menu_class_1'
_b='token_calendar_v3.pickle'
_a='auto Popular'
_Z='auto flash news'
_Y='google calendar'
_X='product'
_W='subtitle'
_V='why us'
_U='description'
_T='location'
_S='priority'
_R='frontend'
_Q='Middle'
_P='posts_updated'
_O='post_deleted'
_N='name'
_M='order_item'
_L='kind'
_K='link'
_J=None
_I='max'
_H='content'
_G='sub title'
_F='photo'
_E='site'
_D='extends'
_C='title'
_B=False
_A=True
import math,os,string
from bs4 import BeautifulSoup as bs
from core.models import ModelList,ModelListSetting,Photo,IconList,OptLogoSettingPos
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.db.models import Max
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_authbox.common import get_site_id
from django_ckeditor_5.fields import CKEditor5Field
from django_cryptography.fields import encrypt
from djmoney.models.fields import MoneyField
from jsonfield import JSONField
from menu.models import Menu
from parler.models import TranslatableModel,TranslatedFields
from uuslug import uuslug
from datetime import datetime,timedelta
from .abstract import BaseAbstractModel
from hitcount.models import HitCountMixin,HitCount
User=get_user_model()
exposed_request=_J
LEN_NAME=100
LEN_TITLE=300
LEN_SUB_TITLE=300
class Logo(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);name=models.CharField(_('logo name'),max_length=LEN_NAME);photo=GenericRelation(Photo);pos=models.SmallIntegerField(choices=OptLogoSettingPos.choices,default=OptLogoSettingPos.TOP_NORMAL)
	class Meta:verbose_name=_('logo');verbose_name_plural=_('logos')
	def __str__(A):return f"{A.name}"
class Favicon(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);name=models.CharField(_('favicon name'),max_length=LEN_NAME);photo=GenericRelation(Photo)
	class Meta:verbose_name=_('favicon');verbose_name_plural=_('favicons')
	def __str__(A):return f"{A.name}"
class OptStatusPublish(models.IntegerChoices):DRAFT=1,_('Draft');PUBLISHED=2,_('Published')
class OptSocialMediaKinds(models.IntegerChoices):FACEBOOK=1,_('Facebook');TWITTER=2,_('Twitter');PINTEREST=3,_('Pinterest');YOUTUBE=4,_('Youtube');INSTAGRAM=5,_('Instagram')
class OptPriority(models.IntegerChoices):HIGH=1,_('High');MIDDLE=2,_(_Q);LOW=3,_('Low')
def word_count(text):A=bs(text,'html.parser');B=A.get_text();return sum([A.strip(string.punctuation).isalpha()for A in B.split()])
def reading_time(wordcount):B=200;C,D=math.modf(wordcount/B);E=1 if C*60>=30 else 0;A=D+E;return 1 if A<=0 else A
class Tags(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);translations=TranslatedFields(name=models.CharField(_('tags name'),max_length=LEN_NAME));slug=models.SlugField(max_length=LEN_NAME,default='',unique=_A,blank=_A,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('tag');verbose_name_plural=_('tags')
	def __str__(A):return f"{A.name}"
	def save(A,*B,**C):A.slug=uuslug(A.name,instance=A,max_length=50);super().save(*(B),**C)
class Categories(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);translations=TranslatedFields(name=models.CharField(_('categories name'),max_length=LEN_NAME));slug=models.SlugField(max_length=LEN_NAME,default='',unique=_A,blank=_A,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('category');verbose_name_plural=_('categories')
	def __str__(A):return f"{A.site.domain} - {A.name}"
	def save(A,*B,**C):A.slug=uuslug(A.name,instance=A,max_length=50);super().save(*(B),**C)
class BaseContentModel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);view_count=models.PositiveIntegerField(_('view count'),default=0,editable=_B);share_count=models.PositiveIntegerField(_('share count'),default=0,editable=_B);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_B);photo=GenericRelation(Photo,verbose_name=_(_F));tags=models.ManyToManyField(Tags,verbose_name=_('tags'),blank=_A);categories=models.ForeignKey(Categories,on_delete=models.PROTECT,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:app_label=_R;abstract=_A
class Announcement(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);priority=models.SmallIntegerField(choices=OptPriority.choices,default=OptPriority.LOW,verbose_name=_(_S));is_header_text=models.BooleanField(default=_B)
	class Meta:verbose_name=_('announcement');verbose_name_plural=_('announcements')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class News(BaseAbstractModel,BaseContentModel,TranslatableModel,HitCountMixin):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);is_header_text=models.BooleanField(default=_B);hit_count_generic=GenericRelation(HitCount,object_id_field='object_pk',related_query_name='hit_count_generic_relation')
	class Meta:verbose_name=_('news');verbose_name_plural=_('news')
	def current_hit_count(A):return A.hit_count.hits
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class Article(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);is_header_text=models.BooleanField(default=_B)
	class Meta:verbose_name=_('article');verbose_name_plural=_('articles')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class Events(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)),location=encrypt(models.CharField(_(_T),max_length=255,null=_A,blank=_A)));word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);is_header_text=models.BooleanField(default=_B);date=models.DateField(_('date'));time=models.TimeField(_('time'))
	class Meta:verbose_name=_('event');verbose_name_plural=_('events')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class SlideShow(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo);translations=TranslatedFields(title=models.CharField(_(_C),max_length=LEN_TITLE),sub_title=models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('slide show');verbose_name_plural=_('slides show')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		super().save(*(B),**C)
class DailyAlert(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);translations=TranslatedFields(alert=encrypt(models.CharField(_('alert'),max_length=500)));link=models.CharField(_(_K),max_length=255,null=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('daily alert');verbose_name_plural=_('daily alerts')
	def __str__(A):return f"{A.alert}"
class WhyUs(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);admin=models.ForeignKey(User,on_delete=models.PROTECT);icon=models.CharField(_('icon'),max_length=100);translations=TranslatedFields(title=models.CharField(_(_C),max_length=LEN_TITLE),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),description=models.CharField(_(_U),max_length=500));is_header_text=models.BooleanField(default=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_(_V);verbose_name_plural=_(_V)
	def __str__(A):return f"{A.icon}"
class Greeting(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo,verbose_name=_(_F));translations=TranslatedFields(title=models.CharField(_(_C),max_length=LEN_TITLE),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)),name=encrypt(models.CharField(_('greeting name'),max_length=LEN_NAME,null=_A,blank=_A)),designation=encrypt(models.CharField(_('designation'),max_length=LEN_NAME,null=_A,blank=_A)));slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A,editable=_B);view_count=models.PositiveIntegerField(default=0,editable=_B);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:verbose_name=_('greeting');verbose_name_plural=_('greetings')
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		super().save(*(B),**C)
class Pages(BaseAbstractModel,BaseContentModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));menu=models.ForeignKey(Menu,on_delete=models.PROTECT,verbose_name='Access From Menu',blank=_A);word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);is_header_text=models.BooleanField(default=_B)
	class Meta:verbose_name=_('page');verbose_name_plural=_('pages')
	def __str__(A):return A.title
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class SocialMedia(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));kind=models.SmallIntegerField(choices=OptSocialMediaKinds.choices,verbose_name=_(_L));link=encrypt(models.URLField(_(_K),max_length=255));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.site.name} - {A.get_kind_display()}"
class BaseGalleryModel(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);view_count=models.PositiveIntegerField(default=0,editable=_B);slug=models.SlugField(max_length=255,default='',unique=_A,blank=_A);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	class Meta:app_label=_R;abstract=_A
class PhotoGallery(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_F))
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		super().save(*(B),**C)
class Fasilities(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_F),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*C,**D):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		if A.order_item==0:
			B=Fasilities.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_M))
			if B:
				if not B[_I]is _J:A.order_item=B[_I]+1
		super().save(*(C),**D)
class Offers(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_F),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*C,**D):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		if A.order_item==0:
			B=Offers.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_M))
			if B:
				if not B[_I]is _J:A.order_item=B[_I]+1
		super().save(*(C),**D)
class HowItWorks(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	icon=models.CharField(_('icon'),max_length=100,null=_A,blank=_A);translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(models.CharField(_(_H),max_length=500,blank=_A,null=_A)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_F),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*C,**D):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		if A.order_item==0:
			B=HowItWorks.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_M))
			if B:
				if not B[_I]is _J:A.order_item=B[_I]+1
		super().save(*(C),**D)
class AboutUs(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(sub_title=encrypt(models.CharField(_(_G),max_length=LEN_TITLE)),title=encrypt(models.CharField(_(_C),max_length=LEN_SUB_TITLE)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));photo=GenericRelation(Photo,verbose_name=_(_F),null=_A,blank=_A)
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		super().save(*(B),**C)
class Testimony(BaseAbstractModel,TranslatableModel):
	translations=TranslatedFields(content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));subtitle=encrypt(models.CharField(_(_W),max_length=LEN_SUB_TITLE));title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE));is_header_text=models.BooleanField(default=_B);photo=GenericRelation(Photo,verbose_name=_(_F),null=_A,blank=_A);site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.title} - {A.subtitle}"
class Product(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(name=encrypt(models.CharField(_(_N),max_length=LEN_NAME)),title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),sub_title=encrypt(models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);icon=models.CharField(max_length=100,null=_A,blank=_A);photo=GenericRelation(Photo,verbose_name=_(_F),null=_A,blank=_A);price=MoneyField(max_digits=10,decimal_places=2,default=0,default_currency='IDR')
	def __str__(A):return f"{A.name}"
	def save(A,*C,**D):
		if not A.slug:A.slug=uuslug(A.name,instance=A,max_length=255)
		if A.order_item==0:
			B=Product.objects.filter(site_id=get_site_id(exposed_request)).aggregate(max=Max(_M))
			if B:
				if not B[_I]is _J:A.order_item=B[_I]+1
		super().save(*(C),**D)
class Cart(BaseAbstractModel):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=_(_X));qty=models.PositiveIntegerField(default=1,blank=_A,editable=_B);site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.product.name}"
class Purchasing(BaseAbstractModel):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name=_(_X));qty=models.PositiveIntegerField(default=1,blank=_A,editable=_B);site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.product.name}"
def save_embed_video(embed):
	E='src';D=0;A='';F=embed.split(' ');B=_B
	for G in F:
		if B:break
		H=G.split('=');B=_B
		for C in H:
			if not B and C.lower()==E:B=_A
			if B and C.lower()!=E:
				if D==0:A+=C;D+=1
				else:A+='='+C
	if A.find('watch')<=0:A=A.replace('"','');A=A.replace('&quot;','');return A
	else:return _J
class VideoGallery(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)));embed=CKEditor5Field(_('embed'),blank=_A,null=_A,config_name=_D);embed_video=models.URLField(blank=_A,null=_A);is_header_text=models.BooleanField(default=_B);order_item=models.PositiveIntegerField(default=0);photo=GenericRelation(Photo,verbose_name=_(_F))
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		A.embed_video=save_embed_video(A.embed);super().save(*(B),**C)
class RelatedLink(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,blank=_A,verbose_name=_(_E));link=encrypt(models.URLField(_(_K),max_length=255));translations=TranslatedFields(name=encrypt(models.CharField(_(_N),max_length=LEN_NAME)));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.name}"
class Document(BaseAbstractModel,BaseContentModel,TranslatableModel):
	file_path_doc=models.FileField(verbose_name=_('file path Document'),upload_to='temp_doc');translations=TranslatedFields(name=encrypt(models.CharField(_(_N),max_length=LEN_NAME)),content=encrypt(CKEditor5Field(_(_H),blank=_A,null=_A,config_name=_D)));word_count=models.PositiveIntegerField(default=0,blank=_A,editable=_B);reading_time=models.PositiveIntegerField(default=0,blank=_A,editable=_B);is_header_text=models.BooleanField(default=_B);size=models.BigIntegerField(_('size'),null=_A,blank=_A,default=0,editable=_B);hits=models.IntegerField(_('hits'),null=_A,blank=_A,default=0,editable=_B)
	def __str__(A):return f"{A.name}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.name,instance=A,max_length=255)
		A.word_count=word_count(A.content);A.reading_time=reading_time(A.word_count);super().save(*(B),**C)
class Popup(BaseAbstractModel,TranslatableModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)));link=encrypt(models.URLField(_(_K),max_length=255,null=_A,blank=_A));photo=GenericRelation(Photo,verbose_name=_(_F));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):return f"{A.title}"
class Banner(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);photo=GenericRelation(Photo,verbose_name=_(_F));link=models.URLField(max_length=255,null=_A,blank=_A);priority=models.SmallIntegerField(choices=OptPriority.choices,default=OptPriority.LOW,verbose_name=_(_S));status=models.SmallIntegerField(choices=OptStatusPublish.choices,default=OptStatusPublish.PUBLISHED)
	def __str__(A):
		B=''
		if A.priority==1:B='High'
		elif A.priority==2:B=_Q
		elif A.priority==3:B='Low'
		B=f"{B} [{A.site.id}] {A.site} {A.link}";return B
class Location(BaseAbstractModel,BaseGalleryModel,TranslatableModel):
	translations=TranslatedFields(title=encrypt(models.CharField(_(_C),max_length=LEN_TITLE)),subtitle=encrypt(models.CharField(_(_W),max_length=LEN_SUB_TITLE)));embed=CKEditor5Field(_('embed'),blank=_A,null=_A,config_name=_D);is_header_text=models.BooleanField(default=_B)
	def __str__(A):return f"{A.title}"
	def save(A,*B,**C):
		if not A.slug:A.slug=uuslug(A.title,instance=A,max_length=255)
		super().save(*(B),**C)
def get_upload_path(instance,filename):
	A=Site.objects.filter(id=instance.site_id)
	if A:A=A.get();A=A.domain
	B=A.split('.')
	if B:B=B[0]
	return os.path.join('credentials',B,'credentials.json')
class GoogleCalendar(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE);calendar_id=models.CharField(_('google calendar ID'),max_length=LEN_NAME);file_path_doc=models.FileField(verbose_name=_('google calendar credentials path'),upload_to=get_upload_path);is_default=models.BooleanField(default=_B)
	class Meta:verbose_name=_(_Y);verbose_name_plural=_('google calendars')
	def __str__(A):return A.calendar_id
class GoogleCalendarDetail(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,blank=_A,null=_A);google_calendar=models.ForeignKey(GoogleCalendar,on_delete=models.CASCADE,verbose_name=_(_Y));event_id=models.CharField(_('google event ID'),max_length=LEN_NAME);start=models.DateTimeField(_('date start'),blank=_A,null=_A);end=models.DateTimeField(_('date end'),blank=_A,null=_A);summary=models.CharField(_('Summary'),max_length=LEN_TITLE,blank=_A,null=_A);description=models.TextField(_(_U),blank=_A,null=_A);cal_name=models.TextField(_('calendar name'),blank=_A,null=_A);visibility=models.CharField(_('visibility'),max_length=LEN_SUB_TITLE,blank=_A,null=_A);location=models.CharField(_(_T),max_length=LEN_SUB_TITLE,blank=_A,null=_A);transparency=models.CharField(_('transparency'),max_length=LEN_SUB_TITLE,blank=_A,null=_A);cal_year=models.PositiveIntegerField(default=2023,blank=_A,editable=_B);cal_month=models.PositiveIntegerField(default=2023,blank=_A,editable=_B);cal_json=JSONField(null=_A,blank=_A)
	class Meta:verbose_name=_('google calendar detail');verbose_name_plural=_('google calendars detail')
	def __str__(A):return f"{A.event_id}"
class Log(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));model_list=models.ForeignKey(ModelList,on_delete=models.CASCADE);is_need_refresh=models.BooleanField(default=_B);expired=models.DateTimeField()
	class Meta:verbose_name=_('log');verbose_name_plural=_('logs')
	def __str__(A):return f"{A.model_list}"
class OptModelKinds(models.IntegerChoices):NEWS=1,_('News');ARTICLE=2,_('Article');ANNOUNCEMENT=3,_('Announcement')
class AutoHeadline(BaseAbstractModel):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);title=models.CharField(_(_C),max_length=LEN_TITLE);sub_title=models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A);slug=models.SlugField(max_length=255,default='',blank=_A,editable=_B);photo=GenericRelation(Photo,verbose_name=_(_F));categories=models.ForeignKey(Categories,on_delete=models.PROTECT,null=_A,blank=_A);kind=models.SmallIntegerField(choices=OptModelKinds.choices,verbose_name=_(_L));is_editable=models.BooleanField(default=_B);created_at=models.DateTimeField(editable=_B)
	class Meta:verbose_name=_('auto headline');verbose_name_plural=_('auto headlines')
	def __str__(A):return f"{A.title}"
class AutoFlashNews(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);title=models.CharField(_(_C),max_length=LEN_TITLE);sub_title=models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A);slug=models.SlugField(max_length=255,default='',blank=_A,editable=_B);photo=GenericRelation(Photo,verbose_name=_(_F));categories=models.ForeignKey(Categories,on_delete=models.PROTECT,null=_A,blank=_A);kind=models.SmallIntegerField(choices=OptModelKinds.choices,verbose_name=_(_L));is_editable=models.BooleanField(default=_B);created_at=models.DateTimeField(editable=_B)
	class Meta:verbose_name=_(_Z);verbose_name_plural=_(_Z)
	def __str__(A):return f"{A.title}"
class AutoPopular(models.Model):
	site=models.ForeignKey(Site,on_delete=models.CASCADE,verbose_name=_(_E));admin=models.ForeignKey(User,on_delete=models.PROTECT);title=models.CharField(_(_C),max_length=LEN_TITLE);sub_title=models.CharField(_(_G),max_length=LEN_SUB_TITLE,null=_A,blank=_A);slug=models.SlugField(max_length=255,default='',blank=_A,editable=_B);photo=GenericRelation(Photo,verbose_name=_(_F));categories=models.ForeignKey(Categories,on_delete=models.PROTECT,null=_A,blank=_A);kind=models.SmallIntegerField(choices=OptModelKinds.choices,verbose_name=_(_L));is_editable=models.BooleanField(default=_B);created_at=models.DateTimeField(editable=_B)
	class Meta:verbose_name=_(_a);verbose_name_plural=_(_a)
	def __str__(A):return f"{A.title}"
@receiver(models.signals.post_delete,sender=Document)
@receiver(models.signals.post_delete,sender=GoogleCalendar)
def auto_delete_file_on_delete(sender,instance,**E):
	A=instance
	if A.file_path_doc:
		if os.path.isfile(A.file_path_doc.path):
			os.remove(A.file_path_doc.path)
			if sender==GoogleCalendar:
				C=os.path.dirname(A.file_path_doc.path);D=_b;B=os.path.join(C,D)
				if os.path.isfile(B):os.remove(B)
@receiver(models.signals.pre_save,sender=Document)
@receiver(models.signals.pre_save,sender=GoogleCalendar)
def auto_delete_file_on_change(sender,instance,**H):
	C=instance;B=sender
	if not C.pk:return _B
	try:A=B.objects.get(pk=C.pk).file_path_doc
	except B.DoesNotExist:return _B
	E=C.file_path_doc
	if not A==E:
		if A:
			if os.path.isfile(A.path):
				os.remove(A.path)
				if B==GoogleCalendar:
					F=os.path.dirname(A.path);G=_b;D=os.path.join(F,G)
					if os.path.isfile(D):os.remove(D)
@receiver(post_delete,sender=Menu,dispatch_uid=_O)
@receiver(post_delete,sender=ModelList,dispatch_uid=_O)
@receiver(post_delete,sender=ModelListSetting,dispatch_uid=_O)
def menu_post_delete_handler(sender,**B):
	A=get_site_id(exposed_request)
	if A>0:cache.delete(_c,version=A);cache.delete(_d,version=A);cache.delete(_e,version=A);cache.delete(_f,version=A);cache.delete(_g,version=A)
@receiver(post_save,sender=Menu,dispatch_uid=_P)
@receiver(post_save,sender=ModelList,dispatch_uid=_P)
@receiver(post_save,sender=ModelListSetting,dispatch_uid=_P)
def menu_post_save_handler(sender,**B):
	A=get_site_id(exposed_request)
	if A>0:cache.delete(_c,version=A);cache.delete(_d,version=A);cache.delete(_e,version=A);cache.delete(_f,version=A);cache.delete(_g,version=A)