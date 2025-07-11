_W='payment_notes'
_V='is_visibled'
_U='subtitle'
_T='file_path_doc'
_S='priority'
_R='description'
_Q='is_editor_choice'
_P='embed'
_O='site_id'
_N='icon'
_M='link'
_L='order_item'
_K='tags'
_J='categories'
_I='is_header_text'
_H='sub_title'
_G='name'
_F='title'
_E='extends'
_D='django_ckeditor_5'
_C='class'
_B='status'
_A='content'
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from core.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column,Layout,Row
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget
from frontend.models import *
from menu.models import Menu
from parler.forms import TranslatableModelForm
class TagsForm(TranslatableModelForm):
	class Meta:model=Tags;fields=[_G,_B]
class WhyUsForm(TranslatableModelForm):
	class Meta:model=WhyUs;fields=[_F,_H,_N,_R,_I,_B]
class LogoForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=300);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=48);save_as_png=forms.CharField(widget=forms.HiddenInput(),initial=1)
	class Meta:model=Logo;fields=[_G,'pos']
class AnnouncementForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Announcement;fields=[_F,_H,_A,_J,_K,_S,_Q,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_O);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_K].queryset=Tags.objects.filter(site_id=site_id);self.fields[_J].queryset=Categories.objects.filter(site_id=site_id)
class GoogleCalendarForm(ModelForm):
	class Meta:model=GoogleCalendar;fields=['calendar_id',_T]
class FasilitiesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Fasilities;fields=[_F,_H,_A,_L,_I,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class OffersForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Offers;fields=[_F,_H,_A,_L,_I,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class NewsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=News;fields=[_F,_H,_A,_J,_K,_I,_Q,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_O);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_K].queryset=Tags.objects.filter(site_id=site_id);self.fields[_J].queryset=Categories.objects.filter(site_id=site_id)
class TestimonyForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=517);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=517)
	class Meta:model=Testimony;fields=[_F,_U,_A,_I,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class ArticleForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Article;fields=[_F,_H,_A,_J,_K,_I,_Q,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_O);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_K].queryset=Tags.objects.filter(site_id=site_id);self.fields[_J].queryset=Categories.objects.filter(site_id=site_id)
class EventsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Events;fields=[_F,'location','date','time',_A,_J,_K,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
	def __init__(self,*args,**kwargs):
		site_id=kwargs.pop(_O);super().__init__(*(args),**kwargs)
		if site_id:self.fields[_K].queryset=Tags.objects.filter(site_id=site_id);self.fields[_J].queryset=Categories.objects.filter(site_id=site_id)
class SlideShowForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=873);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=424)
	class Meta:model=SlideShow;fields=[_F,_H,_A,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class DailyAlertForm(TranslatableModelForm):
	class Meta:model=DailyAlert;fields=['alert',_M,_B]
class GreetingForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=164);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=201)
	class Meta:model=Greeting;fields=[_F,_G,'designation',_A,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class PagesForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Pages;fields=[_F,_H,_A,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class SocialMediaForm(ModelForm):
	class Meta:model=SocialMedia;fields=['kind',_M,_B]
class HowItWorksForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=500);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=624)
	class Meta:model=HowItWorks;fields=[_F,_H,_A,_N,_L,_I,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class AboutUsForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=900);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=600)
	class Meta:model=AboutUs;fields=[_F,_H,_A,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class PhotoGalleryForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=1000);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=496)
	class Meta:model=PhotoGallery;fields=[_F,_A,_L,_I,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class VideoGalleryForm(TranslatableModelForm):
	class Meta:model=VideoGallery;fields=[_F,_P,_B];widgets={_P:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class RelatedLinkForm(TranslatableModelForm):
	class Meta:model=RelatedLink;fields=[_G,_M,_B]
class DocumentForm(TranslatableModelForm):
	class Meta:model=Document;fields=[_G,_A,_T,_J,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class MenuDashboardForm(TranslatableModelForm):
	class Meta:model=Menu;fields=[_G,_V]
class GlobalSettingForm(ModelForm):
	setting_name=forms.CharField(widget=forms.TextInput(),required=False)
	class Meta:model=GlobalSetting;fields=['setting_name',_G]
class MenuForm(TranslatableModelForm):
	class Meta:model=Menu;fields=[_G,_M,'order_menu',_N,_V,'is_external','exclude_menu']
class AgencyForm(TranslatableModelForm):
	class Meta:model=Agency;fields=[_G,'email','phone','fax','whatsapp','address','notes',_W];widgets={'notes':CKEditor5Widget(attrs={_C:_D},config_name=_E),_W:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class CategoriesForm(TranslatableModelForm):
	class Meta:model=Categories;fields=[_G,_B]
class ProductForm(TranslatableModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Product;fields=[_G,_F,_H,_N,'price',_A,_L,_I,_B];widgets={_A:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class TemplateOwnerForm(ModelForm):
	class Meta:model=TemplateOwner;fields=[_G]
class ModelListForm(ModelForm):
	class Meta:model=ModelList;fields=[_G,_R,_B]
class ServiceForm(ModelForm):
	class Meta:model=Service;fields=['site','kind','agency','is_active','expired_date']
class TemplateForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=870);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=500)
	class Meta:model=Template;fields=[_G,'rel_path','template_owner','is_frontend',_B]
class BannerForm(ModelForm):
	dim_w=forms.CharField(widget=forms.HiddenInput(),initial=267);dim_h=forms.CharField(widget=forms.HiddenInput(),initial=417)
	class Meta:model=Banner;fields=[_S,'position',_M]
class LocationForm(TranslatableModelForm):
	class Meta:model=Location;fields=[_F,_U,_P,_I,_B];widgets={_P:CKEditor5Widget(attrs={_C:_D},config_name=_E)}
class CustomUserCreationForm(UserCreationForm):
	is_accept_terms=forms.BooleanField(required=True)
	class Meta(UserCreationForm.Meta):model=get_user_model();fields='email',_G,'is_accept_terms'