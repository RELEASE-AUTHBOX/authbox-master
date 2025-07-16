_Bc='expired_date'
_Bb='is_active'
_Ba='is_frontend'
_BZ='Site is not defind!'
_BY='site name updated'
_BX='Description (en)'
_BW='Description (id)'
_BV='is_external'
_BU='Parent Menu'
_BT='Description'
_BS='select2_update'
_BR='Access From Menu cannot empty!'
_BQ='pages/detail/'
_BP='Access From Menu'
_BO='file_exists'
_BN='FOUND SERVICE'
_BM='agency_id'
_BL='my_active_footer'
_BK='load menu from Cache'
_BJ='load menu from DB'
_BI='CACHES_TIMEOUT'
_BH='count'
_BG='%d %b %y'
_BF='end_date='
_BE='start_date='
_BD='sites'
_BC='why us'
_BB='template_owner'
_BA='template list'
_B9='template owner'
_B8='exclude_menu'
_B7='pagination'
_B6='search'
_B5='related link'
_B4='video gallery'
_B3='photo gallery'
_B2='about us'
_B1='order_item'
_B0='how it works'
_A_='social media'
_Az='designation'
_Ay='daily alert'
_Ax='slide show'
_Aw='order Item'
_Av='result'
_Au='error'
_At='/accounts/logout/'
_As='Group ID Not found!'
_Ar='model list'
_Aq='calendar_id'
_Ap='email'
_Ao='payment_notes'
_An='order_menu'
_Am='Name ('
_Al='embed'
_Ak='fail_add'
_Aj='select2_menu'
_Ai='select2'
_Ah='results'
_Ag='parent_id'
_Af='whyus'
_Ae='modellist'
_Ad='templateowner'
_Ac='related_link'
_Ab='video_gallery'
_Aa='photo_gallery'
_AZ='about_us'
_AY='how_it_works'
_AX='Icon'
_AW='social_media'
_AV='daily_alert'
_AU='slide_show'
_AT='one_record_only'
_AS='Name (en)'
_AR='Name (id)'
_AQ='notes'
_AP='address'
_AO='is_visibled'
_AN='application'
_AM='subtitle'
_AL='Link'
_AK='alert'
_AJ='form not valid '
_AI='is_editor_choice'
_AH='auto_resize'
_AG='site'
_AF='Name'
_AE='text'
_AD='dashboard'
_AC='calendar'
_AB='file_path_doc'
_AA='document'
_A9='Header Text'
_A8='product'
_A7='testimony'
_A6='pages'
_A5='greeting'
_A4='events'
_A3='article'
_A2='news'
_A1='offers'
_A0='Sub Title (en)'
_z='Sub Title (id)'
_y='fasilities'
_x='announcement'
_w='logo'
_v='user'
_u='banner'
_t='link'
_s='location'
_r='template'
_q='Content (en)'
_p='Content (id)'
_o='Title (en)'
_n='Title (id)'
_m='Foto'
_l='tags'
_k='is_header_text'
_j='categories'
_i='language'
_h='Status'
_g='file_path'
_f='save_add'
_e='delete'
_d='form_add'
_c='create.html'
_b='Update'
_a='form_edit'
_Z='save_edit'
_Y='update.html'
_X='Action'
_W='updated_at'
_V='uuid'
_U='sub_title'
_T='status'
_S='service'
_R='icon'
_Q='en'
_P='agency'
_O=True
_N='description'
_M='str_file_path'
_L='photo'
_K='content'
_J='active_page_url'
_I='POST'
_H='name'
_G='form'
_F='title'
_E='active_page'
_D='menu'
_C=None
_B='id'
_A=False
import calendar,datetime
from moneyed import Money
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db import transaction
from django.db.models import Count,F,OuterRef,Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import Truncator
from django.views.generic import TemplateView
from hitcount.models import Hit,HitCount
from menu.menus import Menus
from menu.models import *
from parler.utils import get_active_language_choices
from moneyed.l10n import format_money
from core.forms import *
from core.models import Template
from core.send_email import send_email
from core.tokens import account_activation_token
from core.views import download_image
from django_authbox import msgbox
from django_authbox.common import *
from frontend.models import *
from core.copy_initial_data import do_init_data
from core.management.commands.updatecalendar import update_calendar
from .forms import *
User=get_user_model()
mMsgBox=msgbox.ClsMsgBox()
def save_tags(tag_list,obj_master):
	i=0
	while i<len(tag_list):tag=Tags.objects.get(id=tag_list[i]);obj_master.tags.add(tag);i+=1
class PostLoginView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);self.template_name='allauth/account/'+'post_login.html';return super(PostLoginView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(PostLoginView,self).get_context_data(*(args),**kwargs);context[_E]=get_translated_active_page(_AD);return context
def convert_to_list(data):
	ret=[]
	for i in data:ret.append(int(i))
	return ret
def get_menu_caches(request,caches_name,site_id,active_page,kinds=2,exclude_menu=0,is_visibled=-1):
	print('INSIDE get_menu_caches()');menu_class=_C;menu_list=[];group_id=0
	if kinds==2:
		user_id=request.user.id;obj=User.objects.get(id=user_id);group_id=obj.groups.all()[:1]
		if group_id:group_id=group_id.get().id
		print('==',group_id);model_list=[]
		if group_id<=2:
			temp=Template.objects.filter(site__id=site_id,is_frontend=1)[:1]
			if temp:temp=temp.get().id;model_list=list(ModelListSetting.objects.filter(template_id=temp).values_list('model_list_id',flat=_O))
		else:
			service_id=Service.objects.filter(site_id=site_id);kind_id=_C
			if service_id:kind_id=service_id.get().kind
			if kind_id:
				menu_default=MenuDefault.objects.all()
				for i in menu_default:
					if kind_id in convert_to_list(i.service_option):model_list.append(i.model_list.id)
		if model_list:menu_list=list(ModelList.objects.filter(id__in=model_list).values_list('menu_id',flat=_O))
	elif kinds==1:
		group_id=MenuGroup.objects.filter(site_id=site_id,kind=kinds)
		if group_id:group_id=group_id[0].id
	print('From view backend',group_id,kinds,menu_list,exclude_menu)
	if group_id:menu_class=Menus(group_id,kinds,menu_list,exclude_menu)
	else:print(_As)
	menu=_C;menu_filter=[]
	if menu_class:
		menu=menu_class.get_menus()
		for i in menu:
			if i[_AO]:menu_filter.append(i)
		active_page=active_page.replace('_',' ');menu_active=menu_class.get_active_menu_by_name(active_page)
	else:menu_active=_C
	return{'my_menu':menu_filter,'my_active':menu_active}
def get_menu_caches_footer(request,caches_name,site_id,active_page,kinds=2,exclude_menu=1,parent_name=''):
	caches_timeout=getattr(settings,_BI,12*60*60);menu=cache.get(f"{caches_name}_{kinds}",version=site_id);menu_class=cache.get(f"{caches_name}_class_{kinds}",version=site_id)
	if menu_class is _C:
		print(_BJ);menu_list=[];group_id=0
		if kinds==2:
			user_id=request.user.id;obj=User.objects.get(id=user_id);group_id=obj.groups.all()[:1]
			if group_id:group_id=group_id.get().id
		elif kinds==1:
			group_id=MenuGroup.objects.filter(site_id=site_id,kind=kinds)
			if group_id:group_id=group_id[0].id
		if group_id:menu_class=Menus(group_id,kinds=kinds,exclude_menu=exclude_menu);cache.set(f"{caches_name}_class_{kinds}",menu_class,timeout=caches_timeout,version=site_id)
		else:print(_As)
	else:print(_BK)
	if not menu:
		if menu_class:menu=menu_class.get_menus();cache.set(f"{caches_name}_{kinds}",menu,timeout=caches_timeout,version=site_id)
	parent_id=-1;menu_footer=[]
	if parent_name:
		if menu:
			for i in menu:
				if i[_H].strip().lower()==parent_name.strip().lower():parent_id=i[_B];break
			if parent_id:
				for i in menu:
					if i[_Ag]==parent_id:menu_footer.append(i)
	if menu_class:active_page=active_page.replace('_',' ');menu_active=menu_class.get_active_menu_by_name(active_page)
	else:menu_active=_C
	return{caches_name:menu_footer,_BL:menu_active}
def get_menu_caches_footer2(request,caches_name,site_id,active_page,kinds=2,exclude_menu=1,parent_order=1):
	caches_timeout=getattr(settings,_BI,12*60*60);menu=cache.get(f"{caches_name}_{kinds}",version=site_id);menu_class=cache.get(f"{caches_name}_class_{kinds}",version=site_id)
	if menu_class is _C:
		print(_BJ);menu_list=[];group_id=0
		if kinds==2:
			user_id=request.user.id;obj=User.objects.get(id=user_id);group_id=obj.groups.all()[:1]
			if group_id:group_id=group_id.get().id
		elif kinds==1:
			group_id=MenuGroup.objects.filter(site_id=site_id,kind=kinds)
			if group_id:group_id=group_id[0].id
		if group_id:menu_class=Menus(group_id,kinds=kinds,exclude_menu=exclude_menu);cache.set(f"{caches_name}_class_{kinds}",menu_class,timeout=caches_timeout,version=site_id)
		else:print(_As)
	else:print(_BK)
	if not menu:
		if menu_class:menu=menu_class.get_menus();cache.set(f"{caches_name}_{kinds}",menu,timeout=caches_timeout,version=site_id)
	parent_id=-1;menu_footer=[];parent_name=[]
	if menu:
		for i in menu:
			if not i[_Ag]:parent_name.append(i[_B])
		if not(parent_order>=1 and parent_order<=len(parent_name)):parent_order=1
		parent_id=parent_name[parent_order-1]
		if parent_id:
			for i in menu:
				if i[_B]==parent_id:menu_footer.append(i)
				elif i[_Ag]==parent_id:menu_footer.append(i)
	if menu_class:active_page=active_page.replace('_',' ');menu_active=menu_class.get_active_menu_by_name(active_page)
	else:menu_active=_C
	return{caches_name:menu_footer,_BL:menu_active}
def get_agency(request):
	user=User.objects.filter(id=request.user.id)
	if user:user=user.get();return user.agency.all()
	return _C
def get_template_info(site_id):
	subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_r).values(_g)[:1]);template=Template.objects.filter(site__id=site_id,is_frontend=_O).annotate(file_path=subquery_foto)[:1];print(_r,template)
	if template:return template[0]
	return _C
def get_init_template_id(site_id):
	A='template=';template=Template.objects.filter(site__id=site_id,status=OptStatusPublish.PUBLISHED,is_frontend=_O)[:1];print(A,template)
	if template:template=template.get();print(A,template.id,template.name);return{_B:template.id,_AE:template.name}
	return _C
class IndexView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id(request);print('SITEID = ',self.site_id)
		if self.site_id==-1:print('begin dashboard');return redirect(reverse_lazy(_AD))
		elif self.site_id==-2:print('begin logout');return redirect(_At)
		elif self.site_id==-3 or self.site_id==-31:print('begin user init agency ');return redirect(reverse_lazy('user_init_agency'))
		elif self.site_id==-4 or self.site_id==-41:print('begin user init service');return redirect(reverse_lazy('user_init_service',kwargs={_BM:get_agency_from(request)}))
		else:print('GOTO INDEX DASHBOARD');do_init_data(self.site_id);template=get_template(self.site_id,is_frontend=_A);print('template = ',template);self.template_name=template+'index.html'
		return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(IndexView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_AD);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;context[_r]=get_template_info(self.site_id);context['template_init']=get_init_template_id(self.site_id);context.update(menu);return context
@transaction.atomic
def user_init_agency(request):
	context={};template='smart-admin-2/user_initialize_agency.html';user=User.objects.filter(id=request.user.id)
	if user:
		user=user.get();agency=user.agency.all();context[_P]=agency
		for i in agency:
			if i.is_default:print(_BN);return redirect(f"/dashboard/user/initialize/service/{i.id}")
	else:return redirect(_At)
	if request.method==_I:
		name=request.POST.get('agent-name');agency,created=Agency.objects.language(_B).get_or_create(name=name,defaults={'is_default':_O,_AP:'',_AQ:''})
		if created:agency.set_current_language(_Q);agency.address='';agency.notes='';agency.save()
		print(f"DATA: {agency} - {created}")
		if created:print('ADD AGENCY TO USER');user.agency.add(agency);return redirect(reverse_lazy(_AD))
		else:context[_Au]=f'"{name}" sudah digunakan!'
	print('context',context);return render(request,template,context)
@transaction.atomic
def user_reset_agency(request):
	user=User.objects.filter(id=request.user.id);print(_v,user)
	if user:
		user=user.get();agency=user.agency.all()
		for i in agency:Agency.objects.filter(id=i.id).delete()
		user.agency.clear()
	return redirect(reverse_lazy(_AD))
def user_init_agency_ajax(request,agency_id):
	print('agency_id_ajax',agency_id);user=User.objects.get(id=request.user.id)
	for i in user.agency.filter(is_default=_O):i.is_default=_A;i.save()
	agency=user.agency.filter(id=agency_id)
	if agency:agency=agency.get();agency.is_default=_O;agency.save()
	return JsonResponse({_Av:_O},safe=_A)
@transaction.atomic
def user_connect_agency(request):
	context={};template='smart-admin-2/user_connect_agency.html';user=User.objects.filter(id=request.user.id)
	if user:
		user=user.get();agency=user.agency.all();context[_P]=agency
		for i in agency:
			if i.is_default:print(_BN);return redirect(f"/dashboard/user/initialize/service/{i.id}")
	else:return redirect(_At)
	if request.method==_I:
		code=request.POST.get('agent-code');print('code',code);agency=Agency.objects.filter(shortuuid=code)
		if agency:agency=agency.get();user.agency.add(agency);return redirect(reverse_lazy(_AD))
		else:context[_Au]=f'"{code}" tidak ditemukan!'
	print('context',context);return render(request,template,context)
def user_init_service_ajax(request,agency_id,service_id):
	print('REAL service_id_ajax',agency_id,service_id);mfound=_A;user=User.objects.get(id=request.user.id);agency=user.agency.filter(is_default=_O)[:1]
	if agency:
		agency=agency.get()
		if agency.id==agency_id:print('OKE PARAMETER BENAR');mfound=_O
	if mfound:
		print('clear all is_default service');service=Service.objects.filter(agency_id=agency.id,is_default=_O)
		for i in service:i.is_default=_A;i.save()
		service=Service.objects.filter(id=service_id,agency_id=agency.id)
		if service:service=service.get();service.is_default=_O;service.save()
		return JsonResponse({_Av:_O},safe=_A)
	return JsonResponse({_Av:_A},safe=_A)
@transaction.atomic
def user_init_service(request,agency_id):
	context={};template='smart-admin-2/user_initialize_service.html';context['service_opt']=OptServiceType.choices;service_existing=Service.objects.filter(agency_id=agency_id).order_by('kind');context[_S]=service_existing;context[_BM]=agency_id
	if request.method==_I:
		print('posting data Service ......');service=request.POST.get('select_service');print(_S,service);main_domain=getattr(settings,'MAIN_DOMAIN',request.get_host());user=User.objects.get(id=request.user.id);name=user.email.split('@')[0];agency=Agency.objects.get(id=agency_id)
		if agency:name=agency.name;name=name.replace(' ','');name=name.strip();name=name.lower()
		subdomain=f"{name}.{main_domain}";tgl_exp=datetime.now();tgl_exp=add_months(tgl_exp,1);hostname=request.get_host();print('hostname',hostname)
		if hostname.find('localhost')<0 and hostname.find('127.0.0.1')<0:
			print('Begin create site and sub domain on server');created=_A;mcount=1;tmp=subdomain;site=_C
			while not created:
				site,created=Site.objects.get_or_create(domain=tmp,defaults={_H:name})
				if not created:tmp=f"{name+str(mcount)}.{main_domain}";mcount+=1
			subdomain=tmp;print('Begin Create SUB DOMAIN = ',subdomain)
			if create_sub_domain(name):print('Complete create sub domain')
		else:
			subdomain=hostname;site=Site.objects.filter(domain=hostname)
			if site:site=site.get()
			else:site,created=Site.objects.get_or_create(domain=hostname,defaults={_H:hostname})
			print(_AG,site)
		srv=Service.objects.filter(site_id=site.id)
		if srv:srv=srv.get();context[_Au]=f'Domain "{site.domain}" sudah digunakan oleh service "{srv.get_kind_display()}"! Satu domain hanya dapat digunakan oleh satu service.'
		else:
			srv=Service.objects.create(site_id=site.id,kind=service,agency_id=agency_id,expired_date=tgl_exp,is_active=_O,is_default=_O);template=Template.objects.filter(site=site.id,is_frontend=_O)
			if template:
				for i in template:
					for j in i.site.all():
						if j.id==site.id:i.site.remove(site.id);print(f"DONE remove {site.name} from template {i}")
			template_id=_C;temp=Template.objects.filter(is_frontend=_O)
			for i in temp:
				if service in i.service_option:i.site.add(site);i.save();break
			temp=Template.objects.filter(is_frontend=_A)
			for i in temp:
				if service in i.service_option:i.site.add(site);i.save();break
			print('subdomain',subdomain);group,created=Group.objects.get_or_create(name=subdomain);print(group,created)
			if created:menu_group,created=MenuGroup.objects.get_or_create(site_id=site.id,group_id=group.id)
			group,created=Group.objects.get_or_create(name='Admin');user.groups.add(group);user.save();return redirect(reverse_lazy(_AD))
	return render(request,template,context)
def service_change_ajax(request,service_id):
	print('service_id=',service_id);lst=[];temp=Template.objects.filter(is_frontend=_O)
	for i in temp:
		if service_id in i.service_option:res={};res[_B]=i.id;res[_AE]=i.name;lst.append(res)
	print('res',lst);return JsonResponse({_Ah:lst},safe=_A)
class TagsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'tags.html';return super(TagsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(TagsView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_l);context[_E]=active_page;user=User.objects.get(id=self.request.user.id);agency=user.agency.all();context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def tags_ajax(request):
	site_id=get_site_id(request);obj=Tags();obj.set_current_language(_Q);subquery=Subquery(TagsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));lang=obj.get_current_language();obj2=Tags.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AR]=Truncator(i.name_id).chars(50);res[_AS]=Truncator(i.name).chars(50);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def tags_create(request):
	context={};context[_J]=_l;active_page=get_translated_active_page(_l);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=TagsForm(request.POST)
		if form.is_valid():
			tmp=Tags.objects.filter(translations__name=request.POST.get(_H),site_id=site_id)
			if tmp:messages.info(request,mMsgBox.get(_BO));context[_G]=TagsForm()
			else:post=Tags.objects.language(_B).create(name=request.POST.get(_H),status=request.POST.get(_T),site_id=site_id);post.set_current_language(_Q);post.name=request.POST.get(_H);post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=TagsForm()
	return render(request,template,context)
def tags_update(request,uuid):
	context={};context[_J]=_l;active_page=get_translated_active_page(_l);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TagsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_l))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=TagsForm(instance=post)
	return render(request,template,context)
def tags_delete(request,uuid):context={};site_id=get_site_id(request);data=Tags.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_l))
class LogoView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'logo.html';return super(LogoView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(LogoView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;context[_AT]=_O;active_page=get_translated_active_page(_w);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def logo_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_w).values(_g)[:1]);obj2=Logo.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AF]=Truncator(i.name).chars(50);res['Pos']=i.get_pos_display();res[_m]=i.file_path;res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def logo_create(request):
	context={};context[_J]=_w;active_page=get_translated_active_page(_w);context[_E]=active_page;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_c;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu)
	if request.method==_I:
		form=LogoForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save(commit=_A);post.site_id=site_id;post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_w))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=LogoForm();context[_L]=PhotoForm()
	return render(request,template,context)
def logo_update(request,uuid):
	context={};context[_J]=_w;active_page=get_translated_active_page(_w);context[_E]=active_page;site_id=get_site_id(request);template=get_template(site_id,is_frontend=_A)+_Y;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=LogoForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save(commit=_A);post.site_id=site_id;post.save()
			if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_w))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=LogoForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def logo_delete(request,uuid):context={};site_id=get_site_id(request);data=Logo.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_w))
class AnnouncementView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'announcement.html';return super(AnnouncementView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(AnnouncementView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_x);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def announcement_ajax(request):
	site_id=get_site_id(request);obj=Announcement();obj.set_current_language(_Q);subquery1=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(AnnouncementTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_x).values(_g)[:1]);lang=obj.get_current_language();obj2=Announcement.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res['Priority']=i.get_priority_display();res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def announcement_create(request):
	context={};context[_J]=_x;active_page=get_translated_active_page(_x);context[_E]=active_page;site_id=get_site_id(request);auto_resize=_O;context[_AH]=auto_resize;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=AnnouncementForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST,request.FILES)
		if form.is_valid():
			post=Announcement.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),sub_title=request.POST.get(_U),categories_id=request.POST.get(_j),priority=request.POST.get('priority'),status=request.POST.get(_T),is_editor_choice=form.cleaned_data[_AI],site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_l),post)
			if auto_resize:Photo.objects.create(content_object=post,file_path=request.FILES.get(_g),description=request.POST.get(_N))
			else:Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_x))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=AnnouncementForm(site_id=site_id);context[_L]=PhotoForm()
	return render(request,template,context)
def announcement_update(request,uuid):
	context={};context[_J]=_x;active_page=get_translated_active_page(_x);context[_E]=active_page;site_id=get_site_id(request);auto_resize=_O;context[_AH]=auto_resize;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=AnnouncementForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,request.FILES,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.categories_id=request.POST.get(_j);obj.status=request.POST.get(_T);obj.priority=request.POST.get('priority');obj.is_editor_choice=form.cleaned_data[_AI];obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();obj.tags.clear();save_tags(request.POST.getlist(_l),obj)
			if auto_resize:
				if request.FILES.get(_g):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.FILES.get(_g),description=request.POST.get(_N))
				else:Photo.objects.update(description=request.POST.get(_N))
			elif request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			else:Photo.objects.update(description=request.POST.get(_N))
			set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_x))
	else:
		context[_G]=AnnouncementForm(instance=post,site_id=site_id)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
		messages.info(request,mMsgBox.get(_a))
	return render(request,template,context)
def announcement_delete(request,uuid):context={};site_id=get_site_id(request);data=Announcement.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_x))
class FasilitiesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'fasilities.html';return super(FasilitiesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(FasilitiesView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_y);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def fasilities_ajax(request):
	site_id=get_site_id(request);obj=Fasilities();obj.set_current_language(_Q);subquery1=Subquery(FasilitiesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(FasilitiesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery3=Subquery(FasilitiesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_y).values(_g)[:1]);lang=obj.get_current_language();obj2=Fasilities.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(sub_title_id=subquery3).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title_id).chars(50);res[_A0]=Truncator(i.sub_title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_A9]=i.is_header_text;res[_Aw]=i.order_item;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def fasilities_create(request):
	context={};context[_J]=_y;active_page=get_translated_active_page(_y);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=FasilitiesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			post=Fasilities.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),is_header_text=form.cleaned_data[_k],status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.is_header_text=form.cleaned_data[_k];post.save()
			if request.POST.get(_M):Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_y))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=FasilitiesForm();context[_L]=PhotoForm()
	return render(request,template,context)
def fasilities_update(request,uuid):
	context={};context[_J]=_y;active_page=get_translated_active_page(_y);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Fasilities.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=FasilitiesForm(request.POST,instance=post)
		if post_photo:photo=PhotoForm(request.POST,instance=post_photo)
		else:photo=PhotoForm(request.POST)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.is_header_text=form.cleaned_data[_k];obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_y))
	else:
		context[_G]=FasilitiesForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
		messages.info(request,mMsgBox.get(_a))
	return render(request,template,context)
def fasilities_delete(request,uuid):context={};site_id=get_site_id(request);data=Fasilities.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_y))
class OffersView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'offers.html';return super(OffersView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(OffersView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A1);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def offers_ajax(request):
	site_id=get_site_id(request);obj=Offers();obj.set_current_language(_Q);subquery1=Subquery(OffersTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery3=Subquery(OffersTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery2=Subquery(OffersTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A1).values(_g)[:1]);lang=obj.get_current_language();obj2=Offers.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(sub_title_id=subquery3).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title_id).chars(50);res[_A0]=Truncator(i.sub_title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_A9]=i.is_header_text;res[_Aw]=i.order_item;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def offers_create(request):
	context={};context[_J]=_A1;active_page=get_translated_active_page(_A1);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=OffersForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			post=Offers.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),is_header_text=form.cleaned_data[_k],status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.is_header_text=form.cleaned_data[_k];post.save()
			if request.POST.get(_M):Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A1))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=OffersForm();context[_L]=PhotoForm()
	return render(request,template,context)
def offers_update(request,uuid):
	context={};context[_J]=_A1;active_page=get_translated_active_page(_A1);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Offers.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=OffersForm(request.POST,instance=post)
		if post_photo:photo=PhotoForm(request.POST,instance=post_photo)
		else:photo=PhotoForm(request.POST)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.is_header_text=form.cleaned_data[_k];obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A1))
	else:
		context[_G]=OffersForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
		messages.info(request,mMsgBox.get(_a))
	return render(request,template,context)
def offers_delete(request,uuid):context={};site_id=get_site_id(request);data=Offers.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A1))
class NewsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'news.html';return super(NewsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(NewsView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A2);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def news_ajax(request):
	site_id=get_site_id(request);obj=News();obj.set_current_language(_Q);subquery1=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(NewsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A2).values(_g)[:1]);lang=obj.get_current_language();obj2=News.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res['Header']=i.is_header_text;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def news_create(request):
	context={};context[_J]=_A2;active_page=get_translated_active_page(_A2);context[_E]=active_page;site_id=get_site_id(request);auto_resize=_O;context[_AH]=auto_resize;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=NewsForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST,request.FILES)
		if form.is_valid():
			post=News.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),categories_id=request.POST.get(_j),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id,is_header_text=_O if request.POST.get(_k)=='on'else _A,is_editor_choice=_O if request.POST.get(_AI)=='on'else _A);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_l),post);print('FILE PATH',request.FILES.get(_g))
			if auto_resize:Photo.objects.create(content_object=post,file_path=request.FILES.get(_g),description=request.POST.get(_N))
			else:Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A2))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=NewsForm(site_id=site_id);context[_L]=PhotoForm()
	return render(request,template,context)
def news_update(request,uuid):
	context={};context[_J]=_A2;active_page=get_translated_active_page(_A2);context[_E]=active_page;site_id=get_site_id(request);auto_resize=_O;context[_AH]=auto_resize;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=NewsForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,request.FILES,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.categories_id=request.POST.get(_j);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.is_header_text=_O if request.POST.get(_k)=='on'else _A;obj.is_editor_choice=_O if request.POST.get(_AI)=='on'else _A;obj.save();obj.tags.clear();save_tags(request.POST.getlist(_l),obj)
			if auto_resize:
				if request.FILES.get(_g):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.FILES.get(_g),description=request.POST.get(_N))
				else:Photo.objects.update(description=request.POST.get(_N))
			elif request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			else:Photo.objects.update(description=request.POST.get(_N))
			set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A2))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=NewsForm(instance=post,site_id=site_id)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def news_delete(request,uuid):context={};site_id=get_site_id(request);data=News.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A2))
class ArticleView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'article.html';return super(ArticleView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ArticleView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A3);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def article_ajax(request):
	site_id=get_site_id(request);obj=Article();obj.set_current_language(_Q);subquery1=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(ArticleTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A3).values(_g)[:1]);lang=obj.get_current_language();obj2=Article.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_A9]=i.is_header_text;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def article_create(request):
	context={};context[_J]=_A3;active_page=get_translated_active_page(_A3);context[_E]=active_page;site_id=get_site_id(request);auto_resize=_O;context[_AH]=auto_resize;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=ArticleForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST,request.FILES)
		if form.is_valid():
			post=Article.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),sub_title=request.POST.get(_U),categories_id=request.POST.get(_j),status=request.POST.get(_T),is_header_text=form.cleaned_data[_k],is_editor_choice=form.cleaned_data[_AI],site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_l),post)
			if auto_resize:Photo.objects.create(content_object=post,file_path=request.FILES.get(_g),description=request.POST.get(_N))
			else:Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A3))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=ArticleForm(site_id=site_id);context[_L]=PhotoForm()
	return render(request,template,context)
def article_update(request,uuid):
	context={};context[_J]=_A3;active_page=get_translated_active_page(_A3);context[_E]=active_page;site_id=get_site_id(request);auto_resize=_O;context[_AH]=auto_resize;menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=ArticleForm(request.POST,instance=post,site_id=site_id)
		if post_photo:photo=PhotoForm(request.POST,request.FILES,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.sub_title=request.POST.get(_U);obj.categories_id=request.POST.get(_j);obj.status=request.POST.get(_T);obj.is_header_text=form.cleaned_data[_k];obj.is_editor_choice=form.cleaned_data[_AI];obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();obj.tags.clear();save_tags(request.POST.getlist(_l),obj)
			if auto_resize:
				if request.FILES.get(_g):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.FILES.get(_g),description=request.POST.get(_N))
				else:Photo.objects.update(description=request.POST.get(_N))
			elif request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			else:Photo.objects.update(description=request.POST.get(_N))
			set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A3))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=ArticleForm(instance=post,site_id=site_id)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def article_delete(request,uuid):context={};site_id=get_site_id(request);data=Article.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();set_log_all(site_id,_O);messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A3))
class EventsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'events.html';return super(EventsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(EventsView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A4);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def events_ajax(request):
	site_id=get_site_id(request);obj=Events();obj.set_current_language(_Q);subquery1=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(EventsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A4).values(_g)[:1]);lang=obj.get_current_language();obj2=Events.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def events_create(request):
	context={};context[_J]=_A4;active_page=get_translated_active_page(_A4);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=EventsForm(request.POST,site_id=site_id);photo=PhotoForm(request.POST)
		if form.is_valid():post=Events.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),location=request.POST.get(_s),categories_id=request.POST.get(_j),status=request.POST.get(_T),date=request.POST.get('date'),time=request.POST.get('time'),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.location=request.POST.get(_s);post.save();save_tags(request.POST.getlist(_l),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A4))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=EventsForm(site_id=site_id);context[_L]=PhotoForm()
	return render(request,template,context)
def events_update(request,uuid):
	context={};context[_J]=_A4;active_page=get_translated_active_page(_A4);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=EventsForm(request.POST,instance=post,site_id=site_id);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.location=request.POST.get(_s);obj.categories_id=request.POST.get(_j);obj.status=request.POST.get(_T);obj.date=request.POST.get('date');obj.time=request.POST.get('time');obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();obj.tags.clear();save_tags(request.POST.getlist(_l),obj)
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A4))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=EventsForm(instance=post,site_id=site_id)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def events_delete(request,uuid):context={};site_id=get_site_id(request);data=Events.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A4))
class SlideShowView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'slide_show.html';return super(SlideShowView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(SlideShowView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_Ax);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def slideshow_ajax(request):
	site_id=get_site_id(request);lst=[];obj=SlideShow();obj.set_current_language(_Q);subquery1=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery3=Subquery(SlideShowTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='slideshow').values(_g)[:1]);lang=obj.get_current_language();obj2=SlideShow.objects.language(lang).filter(site_id=site_id).distinct().annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(sub_title_id=subquery3).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title_id).chars(50);res[_A0]=Truncator(i.sub_title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def slideshow_create(request):
	context={};context[_J]=_AU;active_page=get_translated_active_page(_Ax);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=SlideShowForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=SlideShow.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_AU))
		else:print(_AJ);context[_G]=SlideShowForm();context[_L]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=SlideShowForm();context[_L]=PhotoForm()
	return render(request,template,context)
def slideshow_update(request,uuid):
	context={};context[_J]=_AU;active_page=get_translated_active_page(_Ax);context[_E]=active_page;site_id=get_site_id(request);print('site_id slideshow update=',site_id);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.first()
	for i in post.photo.all():print('foto ',i)
	if request.method==_I:
		form=SlideShowForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save()
			if request.POST.get(_M):obj.photo.clear();Photo.objects.create(content_object=obj,file_path=request.POST.get(_M),description=request.POST.get(_N))
			else:print('photo not valid')
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_AU))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=SlideShowForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def slideshow_delete(request,uuid):context={};site_id=get_site_id(request);data=SlideShow.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AU))
class DailyAlertView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'daily_alert.html';return super(DailyAlertView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(DailyAlertView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_Ay);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def dailyalert_ajax(request):
	site_id=get_site_id(request);lst=[];obj=DailyAlert();obj.set_current_language(_Q);subquery1=Subquery(DailyAlertTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_AK));lang=obj.get_current_language();obj2=DailyAlert.objects.language(lang).filter(site_id=site_id).annotate(alert_id=subquery1)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['Alert (id)']=Truncator(i.alert_id).chars(50);res['Alert (en)']=Truncator(i.alert).chars(50);res[_AL]=Truncator(i.link).chars(50);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def dailyalert_create(request):
	context={};context[_J]=_AV;active_page=get_translated_active_page(_Ay);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=DailyAlertForm(request.POST)
		if form.is_valid():post=DailyAlert.objects.language(_B).create(alert=request.POST.get(_AK),link=request.POST.get(_t),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.alert=request.POST.get(_AK);post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_AK)));return redirect(reverse_lazy(_AV))
		else:print(_AJ);context[_G]=DailyAlertForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=DailyAlertForm()
	return render(request,template,context)
def dailyalert_update(request,uuid):
	context={};context[_J]=_AV;active_page=get_translated_active_page(_Ay);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DailyAlertForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.alert=request.POST.get(_AK);obj.link=request.POST.get(_t);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_AK)));return redirect(reverse_lazy(_AV))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=DailyAlertForm(instance=post)
	return render(request,template,context)
def dailyalert_delete(request,uuid):context={};site_id=get_site_id(request);data=DailyAlert.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.alert;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AV))
class GreetingView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(GreetingView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;context[_AT]=_O;active_page=get_translated_active_page(_A5);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def greeting_ajax(request):
	site_id=get_site_id(request);obj=Greeting();obj.set_current_language(_Q);subquery1=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(GreetingTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A5).values(_g)[:1]);lang=obj.get_current_language();obj2=Greeting.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def greeting_create(request):
	context={};context[_J]=_A5;active_page=get_translated_active_page(_A5);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=GreetingForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Greeting.objects.language(_B).create(title=request.POST.get(_F),content=request.POST.get(_K),name=request.POST.get(_H),designation=request.POST.get(_Az),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.name=request.POST.get(_H);post.designation=request.POST.get(_Az);post.save();save_tags(request.POST.getlist(_l),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A5))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=GreetingForm();context[_L]=PhotoForm()
	return render(request,template,context)
def greeting_update(request,uuid):
	context={};context[_J]=_A5;active_page=get_translated_active_page(_A5);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=GreetingForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.content=request.POST.get(_K);obj.name=request.POST.get(_H);obj.designation=request.POST.get(_Az);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A5))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=GreetingForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def greeting_delete(request,uuid):context={};site_id=get_site_id(request);data=Greeting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A5))
class PagesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'pages.html';return super(PagesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(PagesView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A6);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def pages_ajax(request):
	site_id=get_site_id(request);obj=Pages();obj.set_current_language(_Q);subquery1=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery3=Subquery(PagesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A6).values(_g)[:1]);lang=obj.get_current_language();obj2=Pages.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(sub_title_id=subquery3).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title_id).chars(50);res[_A0]=Truncator(i.sub_title).chars(50);res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def menu_already_used(site_id,menu_id):
	A='translations__title';lang=get_active_language_choices()[0];pages=Pages.objects.language(lang).filter(site_id=site_id,menu_id=menu_id).values(A)
	if pages:return pages[0][A]
	return _C
def pages_create(request):
	context={};context[_J]=_A6;active_page=get_translated_active_page(_A6);context[_E]=active_page;context[_Ai]=_BP;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=PagesForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			menu_id=request.POST.get(_Aj)
			if menu_id:
				menu_name_already_used=menu_already_used(site_id,menu_id)
				if not menu_name_already_used:post=Pages.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),menu_id=menu_id,status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();save_tags(request.POST.getlist(_l),post);Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));obj=Menu.objects.get(id=menu_id);obj.link=_BQ+post.slug;obj.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A6))
				else:messages.info(request,mMsgBox.get(_Ak,'Menu already used by '+menu_name_already_used));context[_G]=PagesForm(request.POST);context[_L]=PhotoForm(request.POST)
			else:messages.info(request,mMsgBox.get(_Ak,_BR));context[_G]=PagesForm(request.POST);context[_L]=PhotoForm(request.POST)
	else:messages.info(request,mMsgBox.get(_d));context[_G]=PagesForm();context[_L]=PhotoForm()
	return render(request,template,context)
def pages_update(request,uuid):
	context={};context[_J]=_A6;active_page=get_translated_active_page(_A6);context[_E]=active_page;context[_Ai]=_BP;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	select2_update={_B:post.menu_id,_AE:post.menu.name if post.menu else _C};context[_BS]=select2_update
	if request.method==_I:
		form=PagesForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			menu_id=request.POST.get(_Aj)
			if menu_id:
				lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.menu_id=menu_id;obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();obj.tags.clear();save_tags(request.POST.getlist(_l),obj)
				if photo.is_valid():
					if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
				obj=Menu.objects.get(id=menu_id);obj.link=_BQ+post.slug;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A6))
			else:
				messages.info(request,mMsgBox.get(_Ak,_BR));context[_G]=PagesForm(request.POST,instance=post)
				if post_photo:context[_L]=PhotoForm(request.POST,instance=post_photo)
				else:context[_L]=PhotoForm()
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=PagesForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def pages_delete(request,uuid):context={};site_id=get_site_id(request);data=Pages.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A6))
class SocialMediaView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'social_media.html';return super(SocialMediaView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(SocialMediaView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A_);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def socialmedia_ajax(request):
	site_id=get_site_id(request);obj2=SocialMedia.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['Kind']=i.get_kind_display();res[_AL]=Truncator(i.link).chars(70);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def socialmedia_create(request):
	context={};context[_J]=_AW;active_page=get_translated_active_page(_A_);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=SocialMediaForm(request.POST)
		if form.is_valid():post=form.save(commit=_A);post.site_id=site_id;post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_t)));return redirect(reverse_lazy(_AW))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=SocialMediaForm()
	return render(request,template,context)
def socialmedia_update(request,uuid):
	context={};context[_J]=_AW;active_page=get_translated_active_page(_A_);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=SocialMediaForm(request.POST,instance=post)
		if form.is_valid():post=form.save(commit=_A);post.site_id=site_id;post.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_t)));return redirect(reverse_lazy(_AW))
	else:
		messages.info(request,mMsgBox.get(_a))
		if post:context[_G]=SocialMediaForm(instance=post)
	return render(request,template,context)
def socialmedia_delete(request,uuid):context={};site_id=get_site_id(request);data=SocialMedia.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AW))
class HowItWorksView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'how_it_works.html';return super(HowItWorksView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(HowItWorksView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_B0);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def howitworks_ajax(request):
	site_id=get_site_id(request);obj=HowItWorks();subquery=Subquery(HowItWorksTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(HowItWorksTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery3=Subquery(HowItWorksTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='howitworks').values(_g)[:1]);lang=obj.get_current_language();obj2=HowItWorks.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery).annotate(content_id=subquery2).annotate(sub_title_id=subquery3).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title_id).chars(50);res[_A0]=Truncator(i.sub_title).chars(50);res[_p]=Truncator(i.content_id).chars(70);res[_q]=Truncator(i.content).chars(70);res[_AX]=i.icon;res[_A9]=i.is_header_text;res[_Aw]=i.order_item;res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def howitworks_create(request):
	context={};context[_J]=_AY;active_page=get_translated_active_page(_B0);print(_E,active_page);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=HowItWorksForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():
			post=HowItWorks.objects.language(_B).create(icon=request.POST.get(_R),title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),is_header_text=form.cleaned_data[_k],status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);order_item=request.POST.get(_B1)
			if int(order_item)>0:post.order_item=order_item
			post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_AY))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=HowItWorksForm();context[_L]=PhotoForm()
	return render(request,template,context)
def howitworks_update(request,uuid):
	context={};context[_J]=_AY;active_page=get_translated_active_page(_B0);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=HowItWorks.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=HowItWorksForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.icon=request.POST.get(_R);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.is_header_text=form.cleaned_data[_k];order_item=request.POST.get(_B1)
			if int(order_item)>0:obj.order_item=order_item
			obj.site_id=site_id;obj.admin_id=request.user.id;obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_AY))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=HowItWorksForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def howitworks_delete(request,uuid):context={};site_id=get_site_id(request);data=HowItWorks.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AY))
class AboutUsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'about_us.html';return super(AboutUsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(AboutUsView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_B2);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def aboutus_ajax(request):
	site_id=get_site_id(request);obj=AboutUs();subquery=Subquery(AboutUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(AboutUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery3=Subquery(AboutUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='aboutus').values(_g)[:1]);lang=obj.get_current_language();obj2=AboutUs.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery).annotate(sub_title_id=subquery2).annotate(content_id=subquery3).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(70);res[_o]=Truncator(i.title).chars(70);res[_z]=Truncator(i.sub_title_id).chars(70);res[_A0]=Truncator(i.sub_title).chars(70);res[_p]=Truncator(i.content_id).chars(70);res[_q]=Truncator(i.content).chars(70);res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def aboutus_create(request):
	context={};context[_J]=_AZ;active_page=get_translated_active_page(_B2);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=AboutUsForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=AboutUs.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),content=request.POST.get(_K),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_AZ))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=AboutUsForm();context[_L]=PhotoForm()
	return render(request,template,context)
def aboutus_update(request,uuid):
	context={};context[_J]=_AZ;active_page=get_translated_active_page(_B2);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=AboutUs.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=AboutUsForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo if post_photo else _C)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.content=request.POST.get(_K);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_AZ))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=AboutUsForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def aboutus_delete(request,uuid):context={};site_id=get_site_id(request);data=AboutUs.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AZ))
class TestimonyView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'testimony.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A7);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def testimony_ajax(request):
	site_id=get_site_id(request);obj=Testimony();subquery=Subquery(TestimonyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A7).values(_g)[:1]);lang=obj.get_current_language();obj2=Testimony.objects.language(lang).filter(site_id=site_id).annotate(content_id=subquery).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['Title']=Truncator(i.title).chars(70);res['Sub Title']=Truncator(i.subtitle).chars(70);res[_p]=Truncator(i.content_id).chars(70);res[_q]=Truncator(i.content).chars(70);res[_A9]=i.is_header_text;res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def testimony_create(request):
	context={};context[_J]=_A7;active_page=get_translated_active_page(_A7);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=TestimonyForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=Testimony.objects.language(_B).create(content=request.POST.get(_K),subtitle=request.POST.get(_AM),title=request.POST.get(_F),is_header_text=form.cleaned_data[_k],status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_A7))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=TestimonyForm();context[_L]=PhotoForm()
	return render(request,template,context)
def testimony_update(request,uuid):
	context={};context[_J]=_A7;active_page=get_translated_active_page(_A7);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Testimony.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=TestimonyForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo if post_photo else _C)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.subtitle=request.POST.get(_AM);obj.content=request.POST.get(_K);obj.site_id=site_id;obj.admin_id=request.user.id;obj.is_header_text=form.cleaned_data[_k];obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_A7))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=TestimonyForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def testimony_delete(request,uuid):context={};site_id=get_site_id(request);data=Testimony.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A7))
class PhotoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'photo_gallery.html';return super(PhotoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(PhotoGalleryView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_B3);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def photogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=PhotoGallery();obj.set_current_language(_Q);subquery1=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(PhotoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='photogallery').values(_g)[:1]);lang=obj.get_current_language();obj2=PhotoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(content_id=subquery2).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_p]=Truncator(i.content_id).chars(100);res[_q]=Truncator(i.content).chars(100);res[_m]=i.file_path;res[_A9]=i.is_header_text;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def photogallery_create(request):
	context={};context[_J]=_Aa;active_page=get_translated_active_page(_B3);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=PhotoGalleryForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=PhotoGallery.objects.language(_B).create(title=request.POST.get(_F),status=request.POST.get(_T),content=request.POST.get(_K),site_id=site_id,admin_id=request.user.id,is_header_text=form.cleaned_data[_k]);post.set_current_language(_Q);post.title=request.POST.get(_F);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_Aa))
		else:print(_AJ);context[_G]=PhotoGalleryForm();context[_L]=PhotoForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=PhotoGalleryForm();context[_L]=PhotoForm()
	return render(request,template,context)
def photogallery_update(request,uuid):
	context={};context[_J]=_Aa;active_page=get_translated_active_page(_B3);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=PhotoGalleryForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.status=request.POST.get(_T);obj.content=request.POST.get(_K);obj.site_id=site_id;obj.admin_id=request.user.id;obj.is_header_text=form.cleaned_data[_k];obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_Aa))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=PhotoGalleryForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def photogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=PhotoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_Aa))
def get_video_id(url_video):
	tmp=url_video.split('/')
	if tmp:return tmp[len(tmp)-1]
def download_thumbnail(request,video_id):download_url='https://img.youtube.com/vi/'+video_id+'/mqdefault.jpg';return download_image(request,download_url)
class VideoGalleryView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'video_gallery.html';return super(VideoGalleryView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(VideoGalleryView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_B4);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def videogallery_ajax(request):
	site_id=get_site_id(request);lst=[];obj=VideoGallery();obj.set_current_language(_Q);subquery1=Subquery(VideoGalleryTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model='videogallery').values(_g));lang=obj.get_current_language();obj2=VideoGallery.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(file_path=subquery_foto)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def videogallery_create(request):
	context={};context[_J]=_Ab;active_page=get_translated_active_page(_B4);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=VideoGalleryForm(request.POST)
		if form.is_valid():post=VideoGallery.objects.language(_B).create(title=request.POST.get(_F),embed=request.POST.get(_Al),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.save();video_id=get_video_id(post.embed_video);file_path=download_thumbnail(request,video_id);Photo.objects.create(content_object=post,file_path=file_path,description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_Ab))
		else:print(_AJ);context[_G]=VideoGalleryForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=VideoGalleryForm()
	return render(request,template,context)
def videogallery_update(request,uuid):
	context={};context[_J]=_Ab;active_page=get_translated_active_page(_B4);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=VideoGalleryForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.embed=request.POST.get(_Al);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();video_id=get_video_id(obj.embed_video);file_path=download_thumbnail(request,video_id);obj.photo.clear();Photo.objects.create(content_object=obj,file_path=file_path);messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_Ab))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=VideoGalleryForm(instance=post)
	return render(request,template,context)
def videogallery_delete(request,uuid):context={};site_id=get_site_id(request);data=VideoGallery.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_Ab))
class RelatedLinkView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'related_link.html';return super(RelatedLinkView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(RelatedLinkView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_B5);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def relatedlink_ajax(request):
	site_id=get_site_id(request);lst=[];obj=RelatedLink();obj.set_current_language(_Q);subquery1=Subquery(RelatedLinkTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));lang=obj.get_current_language();obj2=RelatedLink.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AR]=Truncator(i.name_id).chars(50);res[_AS]=Truncator(i.name).chars(50);res[_AL]=Truncator(i.link).chars(70);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def relatedlink_create(request):
	context={};context[_J]=_Ac;active_page=get_translated_active_page(_B5);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=RelatedLinkForm(request.POST)
		if form.is_valid():post=RelatedLink.objects.language(_B).create(name=request.POST.get(_H),link=request.POST.get(_t),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.name=request.POST.get(_H);post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_Ac))
		else:print(_AJ);context[_G]=RelatedLinkForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=RelatedLinkForm()
	return render(request,template,context)
def relatedlink_update(request,uuid):
	context={};context[_J]=_Ac;active_page=get_translated_active_page(_B5);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=RelatedLinkForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.link=request.POST.get(_t);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_Ac))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=RelatedLinkForm(instance=post)
	return render(request,template,context)
def relatedlink_delete(request,uuid):context={};site_id=get_site_id(request);data=RelatedLink.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_Ac))
class DocumentView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'document.html';return super(DocumentView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(DocumentView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_AA);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def document_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Document();obj.set_current_language(_Q);subquery1=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));subquery2=Subquery(DocumentTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));lang=obj.get_current_language();obj2=Document.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(content_id=subquery2)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AR]=Truncator(i.name_id).chars(20);res[_AS]=Truncator(i.name).chars(20);res['content (id)']=Truncator(i.content_id).chars(30);res['content (en)']=Truncator(i.content).chars(30);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def document_create(request):
	context={};context[_J]=_AA;active_page=get_translated_active_page(_AA);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=DocumentForm(request.POST,request.FILES);print('form=',form)
		if form.is_valid():print('categories = ',request.POST.get(_j));print('file = ',request.FILES.get(_AB));post=Document.objects.language(_B).create(name=request.POST.get(_H),content=request.POST.get(_K),file_path_doc=request.FILES.get(_AB),categories_id=request.POST.get(_j),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.name=request.POST.get(_H);post.content=request.POST.get(_K);post.save();print('file_path = ',post.file_path_doc.path);post.size=os.stat(post.file_path_doc.path).st_size;post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_AA))
		else:messages.info(request,mMsgBox.get('form_fail'));context[_G]=DocumentForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=DocumentForm()
	return render(request,template,context)
def document_update(request,uuid):
	context={};context[_J]=_AA;active_page=get_translated_active_page(_AA);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=DocumentForm(request.POST,request.FILES,instance=post)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.content=request.POST.get(_K)
			if request.FILES.get(_AB):obj.file_path_doc=request.FILES.get(_AB)
			obj.status=request.POST.get(_T);obj.categories_id=request.POST.get(_j);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();obj.size=os.stat(obj.file_path_doc.path).st_size;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_AA))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=DocumentForm(instance=post)
	return render(request,template,context)
def document_delete(request,uuid):context={};site_id=get_site_id(request);data=Document.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AA))
class ApplicationView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'application.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super().get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_AN);context[_E]=active_page;menu=get_menu_caches(self.request,_AN,self.site_id,active_page);context.update(menu);return context
def application_ajax(request):
	site_id=get_site_id(request);subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef('ref_template_block__id'),content_type__model='templateblock').values(_g)[:1]);obj2=GlobalSetting.objects.filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_B1);lst=[]
	for i in obj2:print('ref',i.ref_template_block.id);print('template_block',i.file_path);res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=_C;res[_AF]=i.get_name_display();res['Value']=i.value;res[_BT]=i.ref_template_block.description;res[_m]=i.file_path;res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def application_update(request,uuid):
	C='template_block_model_list_id';B='template_id';A='select2_global_setting';context={};context[_J]=_AN;active_page=get_translated_active_page(_AN);context[_E]=active_page;site_id=get_site_id(request);context[A]='Template Block';template_id=get_template_id(site_id);print(B,template_id);context[B]=template_id;menu=get_menu_caches(request,_AN,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=GlobalSetting.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);print('ref template block',post.ref_template_block.id);template_block=TemplateBlock.objects.filter(id=post.ref_template_block.id);template_block_model_list_id='0'
	if template_block:
		template_block=template_block.get()
		for i in template_block.model_list.all():print(C,i.id);template_block_model_list_id=i.id
	context[C]=template_block_model_list_id;tmp_template=get_template(site_id,is_frontend=_O);select2_update_global_setting={_B:post.id,_AE:post.value};context['select2_update_global_setting']=select2_update_global_setting
	if request.method==_I:
		form=GlobalSettingForm(request.POST,instance=post)
		if form.is_valid():
			setting_name=request.POST.get(_H);label='Setting'
			for i in OptSettingName:
				print('--->',i.value,setting_name)
				if i.value==int(setting_name):label=i.label;print('label inside',label);break
			template_block_id=request.POST.get(A);template_block=TemplateBlock.objects.filter(id=template_block_id)
			if template_block:template_block=template_block.get();post.value=tmp_template+template_block.name;post.ref_template_block_id=template_block_id;post.save()
			messages.info(request,mMsgBox.get(_Z,label));return redirect(reverse_lazy(_AN))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=GlobalSettingForm(instance=post)
	return render(request,template,context)
def application_update_ajax(request):
	site_id=get_site_id(request);template=get_template(site_id,is_frontend=_O);search=request.GET.get(_B6);template_id=request.GET.get('t');modellist_id=request.GET.get('ml')
	if search:object_list=TemplateBlock.objects.filter(template_id=template_id,model_list=modellist_id).filter(name__icontains=search).values(_B,text=F(_H))
	else:object_list=TemplateBlock.objects.filter(template_id=template_id,model_list=modellist_id).values(_B,text=F(_H))
	for i in object_list:i[_AE]=template+i[_AE]
	return JsonResponse({_Ah:list(object_list),_B7:{'more':_O}},safe=_A)
class MenuDashboardView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'menu_dashboard.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super().get_context_data(*(args),**kwargs);active_page=get_translated_active_page('menu dashboard');context[_E]=active_page;menu=get_menu_caches(self.request,'menu_dashboard',self.site_id,active_page);context.update(menu);return context
def menu_dashboard_ajax(request):
	user_id=request.user.id;obj=User.objects.get(id=user_id);group_id=obj.groups.all()[:1]
	if group_id:group_id=group_id.get().id
	lst=[]
	if group_id:
		lang=get_active_language_choices()[0];lang2=_B
		if lang==_B:lang2=_Q
		menu=Menus(menu_group=group_id,kinds=2);m_ignore=['media sosial','link terkait',_u,'lokasi'];m_ignore_parent=_C
		if menu:
			obj2=menu.get_menus()
			for i in obj2:
				print(_H,i[_H].lower())
				if i[_H].lower()=='pengaturan':m_ignore_parent=i[_B]
				lvl=i['level']
				if lvl==0 and i[_H].lower()not in m_ignore:continue
				if m_ignore_parent:
					if i[_Ag]==m_ignore_parent:continue
				tmp=''
				while lvl>0:tmp+='_>';lvl-=1
				res={};res[_R]=_C;res[_V]=i[_V];res[_W]=_C;res[_Am+lang+')']=Truncator(i[_H]).chars(50);res[_Am+lang2+')']=Menu.objects.language(lang2).get(pk=i[_B]).name;res['Tree']=tmp+Truncator(i[_H]).chars(70);res[_AL]=Truncator(i[_t]).chars(70);res['Order']=i[_An];res[_AX]=Truncator(i[_R]).chars(50);res['Visibled']=Truncator(i[_AO]).chars(50);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def menu_dashboard_update_ajax(request,uuid):
	data=Menu.objects.filter(uuid=uuid)
	if data:data=data.get();data.is_visibled=not data.is_visibled;data.save();return JsonResponse('True',safe=_A)
	return JsonResponse('False',safe=_A)
class MenuView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'menu.html';return super(MenuView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(MenuView,self).get_context_data(*(args),**kwargs);context[_J]=_D;active_page=get_translated_active_page(_D);context[_E]=active_page;agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_D);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def auto_insert_menu_group(request,domain):
	user_name=request.user.email;tmp=user_name.split('@')
	if len(tmp)>0:print('username',tmp[0]);user_name=tmp[0]
	print('auth group',f"{user_name}.{domain}");post,created=Group.objects.get_or_create(name=f"{user_name}.{domain}");print('post',post,post.id);return post.id
def get_menu_group(request,site_id):
	site_name=Site.objects.get(pk=site_id).domain;print('site_name',site_name);menugroup=MenuGroup.objects.filter(site=site_id,kind=1);print('menugroup',menugroup);menugroup_id=_C
	if not menugroup:group_id=auto_insert_menu_group(request,site_name);menugroup_id=MenuGroup.objects.create(kind=1,site_id=site_id,group_id=group_id);print('menugroup after insert ',menugroup_id)
	if menugroup:return menugroup[0].id
	else:return menugroup_id.id
def menu_ajax(request):
	site_id=get_site_id(request);group_id=get_menu_group(request,site_id);lst=[]
	if group_id:
		lang=get_active_language_choices()[0];lang2=_B
		if lang==_B:lang2=_Q
		print('group_id--',group_id);menu=Menus(menu_group=group_id,kinds=1);print(menu.get_menus())
		if menu:
			obj2=menu.get_menus()
			for i in obj2:
				tmp='';lvl=i['level']
				while lvl>0:tmp+='<i class="fa fa-long-arrow-right"></i> &nbsp;&nbsp;&nbsp;&nbsp; ';lvl-=1
				res={};res[_R]=_C;res[_V]=i[_V];res[_W]=_C;res[_Am+lang+')']=Truncator(i[_H]).chars(50);res[_Am+lang2+')']=Menu.objects.language(lang2).get(pk=i[_B]).name;res['Tree']=tmp+Truncator(i[_H]).chars(70);res[_AL]=Truncator(i[_t]).chars(70);res['Order']=i[_An];res[_AX]=Truncator(i[_R]).chars(50);res['Visibled']=Truncator(i[_AO]).chars(50);res['Exclude']=Truncator(i[_B8]).chars(50);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def menu_create(request):
	context={};context[_J]=_D;active_page=get_translated_active_page(_D);context[_E]=active_page;context[_Ai]=_BU;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);group_id=get_menu_group(request,site_id);menu_group=MenuGroup.objects.get(id=group_id);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=MenuForm(request.POST)
		if form.is_valid():form_clean=form.cleaned_data;post=Menu.objects.language(_B).create(name=form_clean[_H],parent_id=request.POST.get(_Aj),link=form_clean[_t],order_menu=form_clean[_An],icon=form_clean[_R],is_visibled=form_clean[_AO],is_external=form_clean[_BV],exclude_menu=form_clean[_B8]);post.menu_group.add(menu_group);post.set_current_language(_Q);post.name=form_clean[_H];post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_D))
		else:context[_G]=MenuForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=MenuForm()
	return render(request,template,context)
def menu_update(request,uuid):
	context={};context[_J]=_D;active_page=get_translated_active_page(_D);context[_E]=active_page;context[_Ai]=_BU;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);select2_update={_B:post.parent_id,_AE:post.parent.name if post.parent else _C};context[_BS]=select2_update
	if request.method==_I:
		form=MenuForm(request.POST,instance=post)
		if form.is_valid():form_clean=form.cleaned_data;lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.name=form_clean[_H];obj.parent_id=request.POST.get(_Aj);obj.link=form_clean[_t];obj.order_menu=form_clean[_An];obj.icon=form_clean[_R];obj.is_visibled=form_clean[_AO];obj.is_external=form_clean[_BV];obj.exclude_menu=form_clean[_B8];obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_D))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=MenuForm(instance=post)
	return render(request,template,context)
def menu_delete(request,uuid):context={};site_id=get_site_id(request);data=Menu.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_D))
def site_name_update(site_id,name):site=Site.objects.get(id=site_id);site.name=name;site.save()
def get_translated_active_page(active_page):
	ret=active_page;lang=get_active_language_choices()[0];obj=Menu.objects.language(lang).filter(translations__name__iexact=active_page)
	if obj:ret=obj[0].name
	ret=ret.replace(' ','_');ret=ret.lower();print('get_translated_active_page = ',ret);return ret
class AgencyView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'agency.html';return super(AgencyView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(AgencyView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_P);context[_E]=active_page;context[_AT]=_O;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def agency_ajax(request):
	site_id=get_site_id(request);obj=Agency();obj.set_current_language(_Q);service=Service.objects.filter(site_id=site_id).values_list(_P,flat=_O);subquery1=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_AP));subquery2=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_AQ));subquery3=Subquery(AgencyTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_Ao));lang=obj.get_current_language();obj2=Agency.objects.language(lang).filter(id=service[0]).annotate(address_id=subquery1).annotate(notes_id=subquery2).annotate(payment_notes_id=subquery3);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AF]=Truncator(i.name).chars(50);res['Address (id)']=Truncator(i.address_id).chars(50);res['Address (en)']=Truncator(i.address).chars(50);res[_BW]=Truncator(i.notes_id).chars(50);res[_BX]=Truncator(i.notes).chars(50);res['Payment Notes (id)']=Truncator(i.payment_notes_id).chars(50);res['Payment Notes (en)']=Truncator(i.payment_notes).chars(50);res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def agency_create(request):
	context={};context[_J]=_P;active_page=get_translated_active_page(_P);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=AgencyForm(request.POST)
		if form.is_valid():post=Agency.objects.language(_B).create(address=request.POST.get(_AP),notes=request.POST.get(_AQ),payment_notes=request.POST.get(_Ao),name=request.POST.get(_H),email=request.POST.get(_Ap),phone=request.POST.get('phone'),fax=request.POST.get('fax'),whatsapp=request.POST.get('whatsapp'));post.set_current_language(_Q);post.address=request.POST.get(_AP);post.notes=request.POST.get(_AQ);post.payment_notes=request.POST.get(_Ao);post.save();site_name_update(site_id,request.POST.get(_H));print(_BY);messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_P))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=AgencyForm()
	return render(request,template,context)
def agency_update(request,uuid):
	context={};context[_J]=_P;active_page=get_translated_active_page(_P);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=AgencyForm(request.POST,instance=post)
		if form.is_valid():
			lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);new_name=request.POST.get(_H);a=Agency.objects.filter(name__icontains=new_name).exclude(id=obj.id)
			if not a:obj.address=request.POST.get(_AP);obj.notes=request.POST.get(_AQ);obj.payment_notes=request.POST.get(_Ao);obj.name=new_name;obj.email=request.POST.get(_Ap);obj.phone=request.POST.get('phone');obj.fax=request.POST.get('fax');obj.whatsapp=request.POST.get('whatsapp');obj.status=request.POST.get(_T);obj.save();print('site name begin update');site_name_update(site_id,request.POST.get(_H));print(_BY);messages.info(request,mMsgBox.get(_Z,new_name));return redirect(reverse_lazy(_P))
			else:messages.info(request,mMsgBox.get('data_exists',new_name));return redirect(reverse_lazy(_P))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=AgencyForm(instance=post)
	return render(request,template,context)
def agency_delete(request,uuid):context={};site_id=get_site_id(request);data=Agency.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_P))
class CategoriesView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'categories.html';return super(CategoriesView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(CategoriesView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_j);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_j);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def categories_ajax(request):
	site_id=get_site_id(request);obj=Categories();obj.set_current_language(_Q);subquery1=Subquery(CategoriesTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));lang=obj.get_current_language();obj2=Categories.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AR]=Truncator(i.name_id).chars(50);res[_AS]=Truncator(i.name).chars(50);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def categories_create(request):
	context={};context[_J]=_j;active_page=get_translated_active_page(_j);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=CategoriesForm(request.POST)
		if form.is_valid():post=Categories.objects.language(_B).create(name=request.POST.get(_H),status=request.POST.get(_T),site_id=site_id);post.set_current_language(_Q);post.name=request.POST.get(_H);post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=CategoriesForm()
	return render(request,template,context)
def categories_update(request,uuid):
	context={};context[_J]=_j;active_page=get_translated_active_page(_j);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=CategoriesForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_j))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=CategoriesForm(instance=post)
	return render(request,template,context)
def categories_delete(request,uuid):context={};site_id=get_site_id(request);data=Categories.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_j))
class ProductView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'product.html';return super(ProductView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ProductView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_A8);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def product_ajax(request):
	site_id=get_site_id(request);obj=Product();obj.set_current_language(_Q);subquery1=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_H));subquery2=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery3=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_K));subquery4=Subquery(ProductTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_A8).values(_g)[:1]);lang=obj.get_current_language();obj2=Product.objects.language(lang).filter(site_id=site_id).annotate(name_id=subquery1).annotate(title_id=subquery2).annotate(content_id=subquery3).annotate(sub_title_id=subquery4).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AR]=Truncator(i.name_id).chars(50);res[_AS]=Truncator(i.name).chars(50);res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title_id).chars(50);res[_A0]=Truncator(i.sub_title).chars(50);res['price']=format_money(i.price,locale='ID');res[_p]=Truncator(i.content_id).chars(50);res[_q]=Truncator(i.content).chars(50);res[_A9]=i.is_header_text;res[_AX]=i.icon;res[_m]=i.file_path;res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def product_create(request):
	context={};context[_J]=_A8;active_page=get_translated_active_page(_A8);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		photo=PhotoForm(request.POST);form=ProductForm(request.POST)
		if form.is_valid():curr_price=Money(amount=request.POST.get('price_0'),currency=request.POST.get('price_1'));post=Product.objects.language(_B).create(name=request.POST.get(_H),title=request.POST.get(_F),sub_title=request.POST.get(_U),icon=request.POST.get(_R),content=request.POST.get(_K),price=curr_price,is_header_text=form.cleaned_data[_k],status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.name=request.POST.get(_H);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.content=request.POST.get(_K);post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_A8))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=ProductForm();context[_L]=PhotoForm()
	return render(request,template,context)
def product_update(request,uuid):
	context={};context[_J]=_A8;active_page=get_translated_active_page(_A8);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Product.objects.filter(uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	photo=_C
	if request.method==_I:
		if post_photo:photo=PhotoForm(request.POST,instance=post_photo)
		form=ProductForm(request.POST,instance=post)
		if form.is_valid():
			lang=request.POST.get(_i);curr_price=Money(amount=request.POST.get('price_0'),currency=request.POST.get('price_1'));obj=data.get();obj.set_current_language(lang);obj.name=request.POST.get(_H);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.icon=request.POST.get(_R);obj.content=request.POST.get(_K);obj.price=curr_price;obj.is_header_text=form.cleaned_data[_k];obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();print('photo file path',request.POST.get(_M))
			if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_A8))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=ProductForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def product_delete(request,uuid):context={};site_id=get_site_id(request);data=Product.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_A8))
class CalendarView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'calendar.html';return super(CalendarView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(CalendarView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_AC);context[_E]=active_page;context[_AT]=_O;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def calendar_sync_ajax(request):
	site_id=get_site_id(request);site=Site.objects.filter(id=site_id);lst=[]
	if site:site=site.get();site_domain=site.domain;lst.append(site_domain);skrg=datetime.now();lst.append(skrg.month);lst.append(skrg.year);update_calendar(site_domain,skrg.month,skrg.month)
	else:lst.append(_BZ)
	return JsonResponse(lst,safe=_A)
def calendar_sync_all_ajax(request):
	site_id=get_site_id(request);site=Site.objects.filter(id=site_id);lst=[]
	if site:site=site.get();site_domain=site.domain;lst.append(site_domain);update_calendar(site_domain,1,12)
	else:lst.append(_BZ)
	return JsonResponse(lst,safe=_A)
def calendar_ajax(request):
	A='File Path';site_id=get_site_id(request);obj2=GoogleCalendar.objects.filter(site_id=site_id);lst=[]
	for i in obj2:
		res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['calendar Name']=Truncator(i.calendar_id).chars(50)
		if i.file_path_doc:res[A]=Truncator(i.file_path_doc.url).chars(50)
		else:res[A]=_C
		res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def calendar_create(request):
	context={};context[_J]=_AC;active_page=get_translated_active_page(_AC);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=GoogleCalendarForm(request.POST,request.FILES)
		if form.is_valid():post=GoogleCalendar.objects.update_or_create(calendar_id=request.POST.get(_Aq),defaults={_AB:request.FILES.get(_AB),'site_id':site_id});messages.info(request,mMsgBox.get(_f,request.POST.get(_Aq)));return redirect(reverse_lazy(_AC))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=GoogleCalendarForm()
	return render(request,template,context)
def calendar_update(request,uuid):
	context={};context[_J]=_AC;active_page=get_translated_active_page(_AC);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=GoogleCalendar.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=GoogleCalendarForm(request.POST,request.FILES,instance=post)
		if form.is_valid():
			obj=data.get();obj.calendar_id=request.POST.get(_Aq)
			if request.FILES.get(_AB):obj.file_path_doc=request.FILES.get(_AB)
			obj.site_id=site_id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_Aq)));return redirect(reverse_lazy(_AC))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=GoogleCalendarForm(instance=post)
	return render(request,template,context)
def calendar_delete(request,uuid):context={};site_id=get_site_id(request);data=GoogleCalendar.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.calendar_id;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_AC))
def menu_lookup_ajax(request):
	A='translations__name';lang=get_active_language_choices()[0];site_id=get_site_id(request);group_id=get_menu_group(request,site_id);search=request.GET.get(_B6)
	if search:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).filter(translations__name__icontains=search).values(_B,text=F(A))
	else:object_list=Menu.objects.translated(lang).filter(menu_group__id=group_id).values(_B,text=F(A))
	return JsonResponse({_Ah:list(object_list),_B7:{'more':_O}},safe=_A)
class TemplateOwnerView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'template_owner.html';return super(TemplateOwnerView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(TemplateOwnerView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_B9);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def templateowner_ajax(request):
	site_id=get_site_id(request);obj2=TemplateOwner.objects.all();lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AF]=Truncator(i.name).chars(50);res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def templateowner_create(request):
	context={};context[_J]=_Ad;active_page=get_translated_active_page(_B9);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=TemplateOwnerForm(request.POST)
		if form.is_valid():post=TemplateOwner.objects.create(name=request.POST.get(_H));messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_Ad))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=TemplateOwnerForm()
	return render(request,template,context)
def templateowner_update(request,uuid):
	context={};context[_J]=_Ad;active_page=get_translated_active_page(_B9);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=TemplateOwner.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=TemplateOwnerForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.name=request.POST.get(_H);obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_Ad))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=TemplateOwnerForm(instance=post)
	return render(request,template,context)
def templateowner_delete(request,uuid):context={};site_id=get_site_id(request);data=TemplateOwner.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_Ad))
class TemplateView_(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'template.html';return super(TemplateView_,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(TemplateView_,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_BA);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def template_ajax(request):
	site_id=get_site_id(request);subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_r).values(_g)[:1]);obj2=Template.objects.filter(is_frontend=_O).annotate(file_path=subquery_foto);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AF]=Truncator(i.name).chars(50);res['Relative Path']=Truncator(i.rel_path).chars(50);res['Template Owner']=Truncator(i.template_owner).chars(50);res['Frontend']=Truncator(i.is_frontend).chars(50);res[_m]=i.file_path;res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def template_create(request):
	context={};context[_J]=_r;active_page=get_translated_active_page(_BA);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=TemplateForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():tmp=request.POST.get(_BB);post=Template.objects.create(name=request.POST.get(_H),rel_path=request.POST.get('rel_path'),is_frontend=bool(request.POST.get(_Ba)),template_owner_id=tmp if tmp else _C);Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_r))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=TemplateForm();context[_L]=PhotoForm()
	return render(request,template,context)
def template_update(request,uuid):
	context={};context[_J]=_r;active_page=get_translated_active_page(_BA);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Template.objects.filter(uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	print('post_photo',post_photo)
	if request.method==_I:
		form=TemplateForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo if post_photo else _C)
		if form.is_valid():
			obj=data.get();tmp=request.POST.get(_BB);obj.name=request.POST.get(_H);obj.rel_path=request.POST.get('rel_path');obj.is_frontend=bool(request.POST.get(_Ba))
			if tmp:obj.template_owner_id=request.POST.get(_BB)
			obj.save()
			if photo.is_valid():
				if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N))
			messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_r))
	else:
		messages.info(request,mMsgBox.get(_a))
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
		context[_G]=TemplateForm(instance=post)
	return render(request,template,context)
def template_delete(request,uuid):context={};site_id=get_site_id(request);data=Template.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_r))
class ModelListView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'model_list.html';return super(ModelListView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ModelListView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_Ar);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def modellist_ajax(request):
	site_id=get_site_id(request);obj2=ModelList.objects.all();lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_AF]=Truncator(i.name).chars(50);res[_BT]=Truncator(i.description).chars(50);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def modellist_create(request):
	context={};context[_J]=_Ae;active_page=get_translated_active_page(_Ar);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=ModelListForm(request.POST)
		if form.is_valid():post=ModelList.objects.create(name=request.POST.get(_H),description=request.POST.get(_N),status=request.POST.get(_T));messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_Ae))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=ModelListForm()
	return render(request,template,context)
def modellist_update(request,uuid):
	context={};context[_J]=_Ae;active_page=get_translated_active_page(_Ar);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=ModelList.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=ModelListForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.name=request.POST.get(_H);obj.description=request.POST.get(_N);obj.status=request.POST.get(_T);obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_Ae))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=ModelListForm(instance=post)
	return render(request,template,context)
def modellist_delete(request,uuid):context={};site_id=get_site_id(request);data=ModelList.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_Ae))
def is_have_group(request,*group_names):
	u=User.objects.filter(pk=request.user.id)
	if u:
		u=u.get()
		if bool(u.groups.filter(name__in=group_names))|u.is_superuser:return _O
	return _A
class ServiceView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'service.html';return super(ServiceView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ServiceView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_S);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def service_ajax(request):
	is_super_admin=is_have_group(request,['Super Admin'])
	if is_super_admin:obj2=Service.objects.all()
	else:site_id=get_site_id(request);obj2=Service.objects.filter(site_id=site_id)
	lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['Domain']=i.site.domain;res['Service Kind']=i.get_kind_display();res['Agency']=Truncator(i.agency).chars(50);res['Expired Date']=get_natural_datetime(i.expired_date);res['Active']=i.is_active;res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def service_create(request):
	context={};context[_J]=_S;active_page=get_translated_active_page(_S);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		print('request.post');form=ServiceForm(request.POST)
		if form.is_valid():print('form is valid');post=Service.objects.create(site_id=request.POST.get(_AG),kind=request.POST.get('kind'),agency_id=request.POST.get(_P),is_active=bool(request.POST.get(_Bb)),expired_date=request.POST.get(_Bc));print('post=',post);messages.info(request,mMsgBox.get(_f,request.POST.get(_H)));return redirect(reverse_lazy(_S))
		else:print('form-',form)
	else:print('else request.post');messages.info(request,mMsgBox.get(_d));context[_G]=ServiceForm()
	return render(request,template,context)
def service_update(request,uuid):
	context={};context[_J]=_S;active_page=get_translated_active_page(_S);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Service.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=ServiceForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.site_id=request.POST.get(_AG);obj.kind=request.POST.get('kind');obj.agency_id=request.POST.get(_P);obj.is_active=bool(request.POST.get(_Bb));obj.expired_date=request.POST.get(_Bc);obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_S))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=ServiceForm(instance=post)
	return render(request,template,context)
def service_delete(request,uuid):context={};site_id=get_site_id(request);data=Service.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_S))
class BannerView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'banner.html';return super(BannerView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(BannerView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_u);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def banner_ajax(request):
	site_id=get_site_id(request);subquery=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_u).values(_g));obj2=Banner.objects.filter(site_id=site_id).distinct().annotate(file_path=subquery);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['Priority']=i.get_priority_display();res['Position']=i.get_position_display();res[_m]=i.file_path;res[_AL]=Truncator(i.link).chars(70);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def banner_create(request):
	context={};context[_J]=_u;active_page=get_translated_active_page(_u);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=BannerForm(request.POST);photo=PhotoForm(request.POST)
		if form.is_valid():post=form.save(commit=_A);post.site_id=site_id;post.admin_id=request.user.id;post.save();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));messages.info(request,mMsgBox.get(_f,request.POST.get('position')));return redirect(reverse_lazy(_u))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=BannerForm();context[_L]=PhotoForm()
	return render(request,template,context)
def banner_update(request,uuid):
	context={};context[_J]=_u;active_page=get_translated_active_page(_u);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);post_photo=post.photo.all()
	if post_photo:post_photo=post_photo.first()
	if request.method==_I:
		form=BannerForm(request.POST,instance=post);photo=PhotoForm(request.POST,instance=post_photo)
		if form.is_valid():
			post=form.save(commit=_A);post.site_id=site_id;post.admin_id=request.user.id;post.save()
			if request.POST.get(_M):post.photo.clear();Photo.objects.create(content_object=post,file_path=request.POST.get(_M),description=request.POST.get(_N));print('DOne')
			messages.info(request,mMsgBox.get(_Z,request.POST.get('position')));return redirect(reverse_lazy(_u))
	else:
		messages.info(request,mMsgBox.get(_a));context[_G]=BannerForm(instance=post)
		if post_photo:context[_L]=PhotoForm(instance=post_photo)
		else:context[_L]=PhotoForm()
	return render(request,template,context)
def banner_delete(request,uuid):context={};site_id=get_site_id(request);data=Banner.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.link;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_u))
class LocationView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'location.html';return super(LocationView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(LocationView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;context[_AT]=_O;active_page=get_translated_active_page(_s);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def location_ajax(request):
	site_id=get_site_id(request);lst=[];obj=Location();obj.set_current_language(_Q);subquery1=Subquery(LocationTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(LocationTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_AM));lang=obj.get_current_language();obj2=Location.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery1).annotate(subtitle_id=subquery2)
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.subtitle_id).chars(50);res[_A0]=Truncator(i.subtitle).chars(50);tmp=Truncator(i.embed).chars(100);tmp=tmp.replace('<',' ');tmp=tmp.replace('>',' ');res['Embed']=tmp;res[_A9]=i.is_header_text;res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def location_create(request):
	context={};context[_J]=_s;active_page=get_translated_active_page(_s);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=LocationForm(request.POST)
		if form.is_valid():post=Location.objects.language(_B).create(title=request.POST.get(_F),subtitle=request.POST.get(_AM),embed=request.POST.get(_Al),status=request.POST.get(_T),is_header_text=form.cleaned_data[_k],site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.subtitle=request.POST.get(_AM);post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_s))
		else:print(_AJ);context[_G]=LocationForm()
	else:messages.info(request,mMsgBox.get(_d));context[_G]=LocationForm()
	return render(request,template,context)
def location_update(request,uuid):
	context={};context[_J]=_s;active_page=get_translated_active_page(_s);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=Location.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=LocationForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.subtitle=request.POST.get(_AM);obj.embed=request.POST.get(_Al);obj.status=request.POST.get(_T);obj.is_header_text=form.cleaned_data[_k];obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_s))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=LocationForm(instance=post)
	return render(request,template,context)
def location_delete(request,uuid):context={};site_id=get_site_id(request);data=Location.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_s))
class WhyUsView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'why_us.html';return super(WhyUsView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(WhyUsView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_BC);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def whyus_ajax(request):
	site_id=get_site_id(request);obj=WhyUs();obj.set_current_language(_Q);subquery=Subquery(WhyUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_F));subquery2=Subquery(WhyUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_N));subquery3=Subquery(WhyUsTranslation.objects.filter(master_id=OuterRef(_B),language_code=_B).values(_U));lang=obj.get_current_language();obj2=WhyUs.objects.language(lang).filter(site_id=site_id).annotate(title_id=subquery).annotate(description_id=subquery2).annotate(sub_title_id=subquery3);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res[_n]=Truncator(i.title_id).chars(50);res[_o]=Truncator(i.title).chars(50);res[_z]=Truncator(i.sub_title).chars(50);res[_A0]=Truncator(i.sub_title_id).chars(50);res[_BW]=Truncator(i.description_id).chars(100);res[_BX]=Truncator(i.description).chars(100);res[_AX]=Truncator(i.icon).chars(20);res[_h]=i.get_status_display();res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def whyus_create(request):
	context={};context[_J]=_Af;active_page=get_translated_active_page(_BC);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=WhyUsForm(request.POST)
		if form.is_valid():
			tmp=WhyUs.objects.filter(translations__title=request.POST.get(_F),site_id=site_id)
			if tmp:messages.info(request,mMsgBox.get(_BO));context[_G]=WhyUsForm()
			else:post=WhyUs.objects.language(_B).create(title=request.POST.get(_F),sub_title=request.POST.get(_U),description=request.POST.get(_N),icon=request.POST.get(_R),status=request.POST.get(_T),site_id=site_id,admin_id=request.user.id);post.set_current_language(_Q);post.title=request.POST.get(_F);post.sub_title=request.POST.get(_U);post.description=request.POST.get(_N);post.icon=request.POST.get(_R);post.save();messages.info(request,mMsgBox.get(_f,request.POST.get(_F)));return redirect(reverse_lazy(_Af))
	else:messages.info(request,mMsgBox.get(_d));context[_G]=WhyUsForm()
	return render(request,template,context)
def whyus_update(request,uuid):
	context={};context[_J]=_Af;active_page=get_translated_active_page(_BC);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=WhyUs.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=WhyUsForm(request.POST,instance=post)
		if form.is_valid():lang=request.POST.get(_i);obj=data.get();obj.set_current_language(lang);obj.title=request.POST.get(_F);obj.sub_title=request.POST.get(_U);obj.description=request.POST.get(_N);obj.icon=request.POST.get(_R);obj.status=request.POST.get(_T);obj.site_id=site_id;obj.admin_id=request.user.id;obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_F)));return redirect(reverse_lazy(_Af))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=WhyUsForm(instance=post)
	return render(request,template,context)
def whyus_delete(request,uuid):context={};site_id=get_site_id(request);data=WhyUs.objects.filter(site_id=site_id,uuid=uuid);post=get_object_or_404(data);tmp=post.title;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_Af))
class UserView(TemplateView):
	site_id=_C
	def get(self,request,*args,**kwargs):self.site_id=get_site_id(request);template=get_template(self.site_id,is_frontend=_A);self.template_name=template+'user.html';return super(UserView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(UserView,self).get_context_data(*(args),**kwargs);agency=get_agency(self.request);context[_P]=agency;service=[]
		for i in agency:service.append(Service.objects.filter(agency_id=i.id))
		context[_S]=service;active_page=get_translated_active_page(_v);context[_E]=active_page;menu=get_menu_caches(self.request,_D,self.site_id,active_page);context.update(menu);return context
def user_ajax(request):
	site_id=get_site_id(request);obj2=User.objects.filter(site_id=site_id);lst=[]
	for i in obj2:res={};res[_R]=_C;res[_V]=i.uuid;res[_W]=i.updated_at;res['Email']=Truncator(i.email).chars(50);res[_AF]=Truncator(i.name).chars(50);res['Confirm']=i.email_confirmed;res['Site']=i.site.domain;res[_b]=get_natural_datetime(i.updated_at);res[_X]=_C;lst.append(res)
	return JsonResponse(lst,safe=_A)
def user_create(request):
	context={};context[_J]=_v;active_page=get_translated_active_page(_v);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_c
	if request.method==_I:
		form=CustomUserCreationForm(request.POST)
		if form.is_valid():user=form.save(commit=_A);user.site_id=site_id;user.save();current_site=get_current_site(request);subject='Confirm Your Email Address';uid=urlsafe_base64_encode(force_bytes(user.pk));token=account_activation_token.make_token(user);message=render_to_string('account_activation_email.html',{_v:user,'domain':current_site.domain,'uid':uid,'token':token});email_from=getattr(settings,'EMAIL_HOST_USER','noreply@gmail.com');send_email(email_from,'suratiwan03@gmail.com',subject,message);print('email send complete!');return redirect('account_activation_sent')
		else:messages.info(request,mMsgBox.get(_Ak,request.POST.get(_Ap)));context[_G]=CustomUserCreationForm(request.POST)
	else:messages.info(request,mMsgBox.get(_d));context[_G]=CustomUserCreationForm()
	return render(request,template,context)
def user_update(request,uuid):
	context={};context[_J]=_v;active_page=get_translated_active_page(_v);context[_E]=active_page;site_id=get_site_id(request);menu=get_menu_caches(request,_D,site_id,active_page);context.update(menu);template=get_template(site_id,is_frontend=_A)+_Y;data=User.objects.filter(uuid=uuid);post=get_object_or_404(data)
	if request.method==_I:
		form=CustomUserChangeForm(request.POST,instance=post)
		if form.is_valid():obj=data.get();obj.name=request.POST.get(_H);obj.email=request.POST.get(_Ap);obj.save();messages.info(request,mMsgBox.get(_Z,request.POST.get(_H)));return redirect(reverse_lazy(_v))
	else:messages.info(request,mMsgBox.get(_a));context[_G]=CustomUserChangeForm(instance=post)
	return render(request,template,context)
def user_delete(request,uuid):context={};site_id=get_site_id(request);data=User.objects.filter(uuid=uuid);post=get_object_or_404(data);tmp=post.name;post.delete();messages.info(request,mMsgBox.get(_e,tmp));return redirect(reverse_lazy(_v))
def get_hitcount_daily(request):
	A='created__date';lst=[];tgl=datetime.now();site_id=get_site_id(request);content_type_id=ContentType.objects.get(app_label=_BD,model=_AG);content_type_id=content_type_id.id if content_type_id else _C;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _C;start_date=add_months(tgl,-3);start_date=datetime(start_date.year,start_date.month,1,0,0,0);print(_BE,start_date);res=calendar.monthrange(tgl.year,tgl.month);day=res[1];end_date=datetime(tgl.year,tgl.month,day,23,59,59);print(_BF,end_date);hit=Hit.objects.filter(hitcount_id=hitcount_id,created__range=[start_date,end_date]).values(A).annotate(count=Count(_B)).order_by(A);cat=[];val=[]
	for i in hit:tmp=[];dtime=i[A];cat.append(dtime.strftime(_BG));val.append(i[_BH])
	lst.append(cat);lst.append(val);return lst
def get_hitcount_monthly(request):
	B='created__month';A='created__year';lst=[];tgl=datetime.now();site_id=get_site_id(request);content_type_id=ContentType.objects.get(app_label=_BD,model=_AG);content_type_id=content_type_id.id if content_type_id else _C;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _C;start_date=add_months(tgl,-3);start_date=datetime(start_date.year,start_date.month,1,0,0,0);print(_BE,start_date);res=calendar.monthrange(tgl.year,tgl.month);day=res[1];end_date=datetime(tgl.year,tgl.month,day,23,59,59);print(_BF,end_date);hit=Hit.objects.filter(hitcount_id=hitcount_id,created__range=[start_date,end_date]).values(A,B).annotate(count=Count(_B)).order_by(A,B);print(hit);cat=[];val=[]
	for i in hit:tmp=[];dtime=i[B];dtime_year=i[A];cat.append(calendar.month_abbr[dtime]+' '+str(dtime_year));val.append(i[_BH])
	lst.append(cat);lst.append(val);return lst
def get_hitcount_weekly(request):
	lst=[];tgl=datetime.now();site_id=get_site_id(request);content_type_id=ContentType.objects.get(app_label=_BD,model=_AG);content_type_id=content_type_id.id if content_type_id else _C;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _C;start_date=add_months(tgl,-3);start_date=datetime(start_date.year,start_date.month,1,0,0,0);print(_BE,start_date);res=calendar.monthrange(tgl.year,tgl.month);day=res[1];end_date=datetime(tgl.year,tgl.month,day,23,59,59);print(_BF,end_date);hit=Hit.objects.filter(hitcount_id=hitcount_id,created__range=[start_date,end_date]);week_begin,week_end=get_week_date(tgl.year,tgl.month,tgl.day);cat=[];val=[]
	for i in range(13):
		week_begin_2=week_begin-timedelta(days=7*i);week_end_2=week_end-timedelta(days=7*i);week_end_2=datetime(week_end_2.year,week_end_2.month,week_end_2.day,23,59,59);hit_2=hit.filter(created__range=[week_begin_2,week_end_2]).values('domain').annotate(count=Count(_B))
		if hit_2:
			for j in hit_2:cat.insert(0,week_begin_2.strftime(_BG)+' - '+week_end_2.strftime(_BG));val.insert(0,j[_BH])
	lst.append(cat);lst.append(val);return lst
def hitcount_ajax(request,period='2'):
	lst=[]
	if period=='2':lst=get_hitcount_daily(request)
	elif period=='3':lst=get_hitcount_weekly(request)
	elif period=='4':lst=get_hitcount_monthly(request)
	return JsonResponse(lst,safe=_A)
def template_lookup_ajax(request,service_id):
	search=request.GET.get(_B6);template=Template.objects.filter(service_option__contains=service_id,is_frontend=_O,status=OptStatusPublish.PUBLISHED)
	if search:object_list=template.filter(name__icontains=search).values(_B,text=F(_H))
	else:object_list=template.values(_B,text=F(_H))
	return JsonResponse({_Ah:list(object_list),_B7:{'more':_O}},safe=_A)
def template_photo_ajax(request,template_id):subquery_foto=Subquery(Photo.objects.filter(object_id=OuterRef(_B),content_type__model=_r).values(_g)[:1]);object_list=Template.objects.filter(id=template_id).values(_L).annotate(file_path=subquery_foto);return JsonResponse(list(object_list),safe=_A)
@transaction.atomic
def template_change(request,template_id):
	site_id=get_site_id(request);template=Template.objects.filter(is_frontend=_O,site__id=site_id)
	for i in template:i.site.remove(site_id)
	print(_r,template);template=Template.objects.filter(id=template_id)
	if template:template=template.get();template.site.add(site_id);print('selesai');return JsonResponse('True',safe=_A)
	return JsonResponse('False',safe=_A)
def set_log_all(site_id,is_need_refresh):set_log(site_id,'Auto Headline',is_need_refresh);set_log(site_id,'Article Notes',is_need_refresh);set_log(site_id,'Flash News',is_need_refresh);set_log(site_id,'Auto Popular',is_need_refresh);set_log(site_id,'Related News',is_need_refresh);set_log(site_id,'Auto Headline Editor Choice',is_need_refresh)
def set_log(site_id,model_name,is_need_refresh):
	model_list=ModelList.objects.filter(name=model_name)[:1]
	if not model_list:raise Http404("Model List '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(model_name,'/admin'))
	model_list=model_list[0];print(_Ar,model_list);tmp_log=Log.objects.filter(site_id=site_id,model_list=model_list);print('tmp_log',tmp_log)
	if tmp_log:post=tmp_log[0];post.is_need_refresh=is_need_refresh;post.save();print('save complete',post)