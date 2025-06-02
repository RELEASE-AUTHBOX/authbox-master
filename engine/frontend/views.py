_AD='random_model'
_AC='random_paint'
_AB='latest_kind'
_AA='tags_list'
_A9='categories_list'
_A8='autoheadline'
_A7='translations__name'
_A6='videogallery'
_A5='description'
_A4='Asia/Makassar'
_A3='latest_news'
_A2='latest_announcement'
_A1='content_detail'
_A0="Menu Group '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_z='baseurl'
_y='format_date'
_x='logo_bottom_dark'
_w='logo_bottom_normal'
_v='logo_top_dark'
_u='logo_top_normal'
_t='Halaman tidak ditemukan!'
_s='all'
_r='start'
_q='booking.html'
_p='location'
_o='count'
_n='testimony'
_m='aboutus'
_l='id'
_k='/dashboard'
_j='pages'
_i='document'
_h='howitworks'
_g='pagetype'
_f='name'
_e='proses'
_d='menugroup'
_c="service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_b='greeting'
_a='product'
_Z='offers'
_Y='fasilities'
_X='socialmedia'
_W='relatedlink'
_V='menu'
_U='home'
_T='slug'
_S='order_item'
_R='/admin'
_Q='events'
_P='slideshow'
_O='logo'
_N='base_url'
_M='is_mobile'
_L='photogallery'
_K='-created_at'
_J='kind'
_I='article'
_H='frontend'
_G=True
_F='-updated_at'
_E='news'
_D='-is_header_text'
_C='announcement'
_B=False
_A=None
import calendar,datetime,random,shutil
from django.utils import timezone
from dateutil.parser import parse
from django_authbox.common import get_natural_datetime,get_format_date
from django.shortcuts import redirect
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count,OuterRef,Subquery,Value
from django.http import Http404,JsonResponse
from django.views.generic import TemplateView
from hitcount.models import Hit,HitCount
from hitcount.views import HitCountMixin
from menu.models import MenuGroup
from parler.utils import get_active_language_choices
from django.utils.text import Truncator
from backend.views import get_menu_caches,get_translated_active_page,get_menu_caches_footer,get_menu_caches_footer2
from core.common import get_agency_info,get_agency_meta
from core.models import OptSettingName,GlobalSetting,TemplateBlock
from django_authbox.common import add_months,get_site_id_front,get_template,get_template_id,get_week_date
from django_authbox.views import service_exists
from django.conf import settings
from .models import *
from django.utils.html import strip_tags
from frontend.Google import *
from core.management.commands.updatecalendar import update_calendar
from hitcount.views import HitCountDetailView
def get_calendar_id(site_id):
	obj=GoogleCalendar.objects.filter(site_id=site_id)[:1]
	if obj:obj=obj.get();return obj.calendar_id
	return _A
def get_calendar_ajax(request,year,month):
	site_id=get_site_id_front(request);res=[];calendar_id=get_calendar_id(site_id);timeZone=_A4;bg_color=['rgb(220, 235, 252)','rgb(173, 209, 245)','rgb(129, 180, 237)','rgb(38, 101, 167)','rgb(0, 116, 217)'];bg_cal_name=[];TZA=pytz.timezone(timeZone);res=[];gc=GoogleCalendar.objects.filter(calendar_id=calendar_id)[:1]
	if gc:
		gcd=GoogleCalendarDetail.objects.filter(cal_year=year,cal_month=month,site_id=site_id,google_calendar=gc).order_by(_r)
		for i in gcd:
			if i.cal_name not in bg_cal_name:bg_cal_name.append(i.cal_name)
			tmp_color=-1
			for (j,name) in enumerate(bg_cal_name):
				if name==i.cal_name:tmp_color=j
			if tmp_color>=len(bg_color):tmp_color=-1
			tmp={'title':i.summary,_r:i.start.astimezone(TZA).isoformat(),'end':i.end.astimezone(TZA).isoformat(),'desc':i.description,'eventBackgroundColor':''if tmp_color<0 else bg_color[tmp_color]};res.append(tmp)
	return JsonResponse(res,safe=_B)
def get_menu_group(site_id):
	menugroup=MenuGroup.objects.filter(site_id=site_id,kind=1)
	if menugroup:return menugroup[0].id
	else:raise Http404("Menu Group belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_k)
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef(_l),content_type__model=model_name).values('file_path')[:1])
def get_photo_desc(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef(_l),content_type__model=model_name).values(_A5)[:1])
def get_logo(site_id,max_data=1):
	subquery_foto=get_photo(_O);logo=Logo.objects.filter(site_id=site_id).values(_f).annotate(file_path=subquery_foto)[:max_data]
	if logo:return logo
	return _A
def get_logo_pos(site_id,options):
	subquery_foto=get_photo(_O);logo=Logo.objects.filter(site_id=site_id).values(_f).annotate(file_path=subquery_foto).filter(pos=options)
	if logo:return logo[0]
	return _A
def get_base_url(request,path_count=0):
	A='/';my_path=request.path.split(A)
	if my_path:
		if len(my_path)>2:
			if not path_count:return my_path[0]+A+my_path[1]+A+my_path[2]
			tmp=''
			for i in range(0,path_count+1):tmp+=my_path[i]+A
			return tmp
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def get_statistic(site_id,is_cache=_B):
	C='user_agent';B=')';A='load from DB (';context={};tgl=datetime.datetime.now();content_type_id=ContentType.objects.get(app_label='sites',model='site');content_type_id=content_type_id.id if content_type_id else _A;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _A;tgl00=tgl+datetime.timedelta(days=1);jam00=datetime.datetime(tgl00.year,tgl00.month,tgl00.day,0,1,0);timeout=(jam00-tgl00).seconds;selisih=0;tmp='hit_today';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):hit_today=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day);tmp_cache=hit_today.count()if hit_today else 1;cache.set(tmp,tmp_cache,timeout,version=site_id);context[tmp]=tmp_cache
	else:hit_today=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day);context[tmp]=hit_today.count()if hit_today else 1;selisih=context[tmp]-tmp_cache;
	tmp='hit_yesterday';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):start_date=tgl+datetime.timedelta(days=-1);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=start_date.year,created__month=start_date.month,created__day=start_date.day).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;tmp='hit_this_week';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):start_date,end_date=get_week_date(tgl.year,tgl.month,tgl.day);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;tmp='hit_last_week';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):start_date,end_date=get_week_date(tgl.year,tgl.month,tgl.day);start_date=start_date+datetime.timedelta(days=-7);end_date=end_date+datetime.timedelta(days=-7);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;tmp='hit_this_month';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;tmp='hit_last_month';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):start_date=add_months(tgl,-1);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=start_date.year,created__month=start_date.month).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;start_date=tgl+datetime.timedelta(hours=-5);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour,0,0);end_date=datetime.datetime(tgl.year,tgl.month,tgl.day,tgl.hour,59,59);hit_online=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).values(C).order_by(C).distinct();context['hit_online']=hit_online.count()if hit_online else 1;tmp='hit_all';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):hit_count=HitCount.objects.filter(object_pk=site_id,content_type_id=content_type_id);tmp_cache=hit_count[0].hits if hit_count else 1;cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;return context
def get_model_content(site_id,lang,model,kind,max_data):
	subquery_foto=get_photo(kind);obj=model.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
	for i in obj:i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_banner(site_id,max_data=3):subquery_foto=get_photo('banner');return Banner.objects.filter(site_id=site_id).annotate(file_path=subquery_foto)[:max_data]
def get_announcement(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_C);obj=Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by('priority',_F)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_slideshow(site_id,lang,max_data=5,is_random=_B):
	subquery_foto=get_photo(_P);obj=SlideShow.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_F)[:max_data]
	if is_random:obj=list(obj);random.shuffle(obj)
	return obj
def get_fasilities(site_id,lang,exclude_id=[],is_header_text=_A,is_shuffle=_A):
	subquery_foto=get_photo(_Y)
	if is_header_text is _A:obj=Fasilities.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).annotate(file_path=subquery_foto).order_by(_D,_S)[:10];
	else:obj=Fasilities.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).exclude(is_header_text=is_header_text).annotate(file_path=subquery_foto).order_by(_D,_S)[:10]
	obj=list(obj)
	if is_shuffle:random.shuffle(obj)
	return obj
def get_offers(site_id,lang,exclude_id=[],is_header_text=_A,is_shuffle=_A):
	subquery_foto=get_photo(_Z)
	if is_header_text is _A:obj=Offers.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).annotate(file_path=subquery_foto).order_by(_D,_S)[:10]
	else:obj=Offers.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).exclude(is_header_text=_G).annotate(file_path=subquery_foto).order_by(_D,_S)[:10]
	return obj
def get_whyus(site_id,lang,max_data=3):return WhyUs.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_D,_F)[:max_data]
def get_dailyalert(site_id,lang,max_data=3):return DailyAlert.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_F)[:max_data]
def get_howitworks(site_id,lang,max_data=3,max_words=20):
	obj=HowItWorks.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_D,_S)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_aboutus(site_id,lang,max_data=1,max_words=100):subquery_foto=get_photo(_m);obj=AboutUs.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_l)[:max_data];return obj
def get_testimony(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_n);obj=Testimony.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_product(site_id,lang,max_data=3,max_words=20):subquery_foto=get_photo(_a);obj=Product.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_S)[:max_data];return obj
def get_greeting(site_id,lang,max_data=1):subquery_foto=get_photo(_b);return Greeting.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_F)[:max_data]
def get_events(site_id,lang,max_data=3):subquery_foto=get_photo(_Q);return Events.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
def get_photogallery(site_id,lang,max_data=16):subquery_foto=get_photo(_L);return PhotoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_S)[:max_data]
def get_videogallery(site_id,lang,max_data=16):subquery_foto=get_photo(_A6);return VideoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
def get_relatedlink(site_id,lang,max_data=3):return RelatedLink.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_F)[:max_data]
def get_news(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_E);obj=News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_article(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_I);obj=Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_document(site_id,lang,max_data=3,max_words=20):
	obj=Document.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_D,_F)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_socialmedia(site_id,max_data=5):return SocialMedia.objects.filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_F)[:max_data]
def get_categories_list(site_id,lang,max_data,model):
	A='categories_id';subquery=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values(_A7)[:1]);subquery_slug=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values(_T)[:1]);categories_list=[];obj=model.objects.filter(site_id=site_id).values(A).annotate(count=Count(A)).annotate(name=subquery).annotate(slug=subquery_slug).order_by(A)[:max_data]
	if obj:
		all_data=0
		for i in obj:all_data+=i[_o]
		categories_list=list(obj);categories_all={A:0,_o:all_data,_f:'All',_T:_s};categories_list.insert(0,categories_all);return categories_list
def get_tags_list(site_id,lang,max_data,model):
	site_name={f"{model.__name__.lower()}__site":f"{site_id}"};val=f"{model.__name__.lower()}__tags";subquery=Subquery(Tags.objects.translated(lang).filter(id=OuterRef(val)).values(_A7)[:1]);subquery_slug=Subquery(Tags.objects.translated(lang).filter(id=OuterRef(val)).values(_T)[:1]);tags_list=[];obj=model.tags.through.objects.filter(**site_name).values(val).annotate(count=Count(val)).annotate(name=subquery).annotate(slug=subquery_slug).order_by(val)[:max_data]
	if obj:
		all_data=0
		for i in obj:all_data+=i[_o]
		tags_list=list(obj);tags_all={'tags_id':0,_o:all_data,_f:'All',_T:_s};tags_list.insert(0,tags_all);return tags_list
def get_latest_model(site_id,lang,max_data,model,kind,exclude_slug=_A):
	subquery_foto=get_photo(kind)
	if exclude_slug:return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).exclude(slug=exclude_slug).order_by(_D,_F)[:max_data]
	return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_D,_F)[:max_data]
def get_random_items(qs,max_data):possible_ids=list(qs.values_list(_l,flat=_G));req_no_of_random_items=len(possible_ids)+1 if len(possible_ids)+1<max_data else max_data;possible_ids=random.choices(possible_ids,k=req_no_of_random_items);return qs.filter(pk__in=possible_ids)
def get_related_model(site_id,lang,max_data,model,kind,exclude_slug=_A):
	subquery_foto=get_photo(kind)
	if exclude_slug:qs=model.objects.translated(lang).filter(site_id=site_id,is_header_text=_B).exclude(slug=exclude_slug)
	else:qs=model.objects.translated(lang).filter(site_id=site_id,is_header_text=_B)
	if qs:random_paint=get_random_items(qs,max_data);random_paint=random_paint.annotate(file_path=subquery_foto);header_text=model.objects.translated(lang).filter(site_id=site_id,is_header_text=_G).annotate(file_path=subquery_foto);return (header_text|random_paint).order_by(_D)
def get_content_detail(site_id,lang,model,kind,slug):
	subquery_foto=get_photo(kind);subquery_foto_desc=get_photo_desc(kind);obj=model.objects.translated(lang).filter(site_id=site_id,slug=slug).annotate(file_path=subquery_foto).annotate(foto_description=subquery_foto_desc)
	if obj:obj=obj.get();obj.created_at=get_natural_datetime(obj.created_at);return obj
	raise Http404(_t)
def get_content_list(site_id,lang,model,kind,slug):
	if not slug:raise Http404(_t)
	field_is_header_text_exists=_B
	for field in model._meta.get_fields():
		if field.name=='is_header_text':field_is_header_text_exists=_G;break
	subquery_foto=get_photo(kind)
	if slug==_s:
		if field_is_header_text_exists:return model.objects.translated(lang).filter(site_id=site_id,is_header_text=_B).annotate(file_path=subquery_foto).order_by(_K)
		return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_K)
	else:
		categories=Categories.objects.filter(slug=slug);categories=categories.get()if categories else _A
		if categories:
			if field_is_header_text_exists:return model.objects.translated(lang).filter(site_id=site_id,categories_id=categories.id,is_header_text=_B).annotate(file_path=subquery_foto).order_by(_K)
			return model.objects.translated(lang).filter(site_id=site_id,categories_id=categories.id).annotate(file_path=subquery_foto).order_by(_K)
		raise Http404('Categories '+slug+' tidak ditemukan!')
def get_location(site_id,lang,max_data=2):return Location.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_D,_F)[:max_data]
def get_og(site_id):
	ret={};ret['og_type']='website';site=Site.objects.get(id=site_id)
	if site:ret['og_url']=site.domain
	return ret
def set_setting(site_id,setting_id):
	template_id=get_template_id(site_id);template=get_template(site_id);template_block=TemplateBlock.objects.filter(template_id=template_id,price_level=1,status=OptStatusPublish.PUBLISHED);label=''
	for i in OptSettingName:
		if i.value==setting_id:label=i.label;break
	ret=_A
	for i in template_block:
		if str(label)in[j.name for j in i.model_list.all()]:ret=template+i.name;GlobalSetting.objects.create(site_id=site_id,name=setting_id,value=ret,ref_template_block_id=i.id);break
	return ret
def get_setting(site_id,setting_id):
	global_setting=GlobalSetting.objects.filter(site_id=site_id,name=setting_id);
	if global_setting:return global_setting[0].value
	return set_setting(site_id,setting_id)
class IndexView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		hostname=request.get_host();hostname_split=hostname.strip().split('.')
		if hostname_split[0]=='www':hostname_split.pop(0);hostname='.'.join(hostname_split);return redirect(f"https://{hostname}")
		service=service_exists(request);service_type=service;
		if not service_type:raise Http404("service belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_R)
		self.site_id=get_site_id_front(request)
		if request.session.session_key:obj=Site.objects.get(id=self.site_id)
		template=get_template(self.site_id);self.template_name=template+'index.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*(args),**kwargs);context[_g]='index';context['menu_justify']='right';context['agency_meta']=get_agency_meta(self.request,self.site_id);context[_M]=self.request.device[_M];
		for i in OptSettingName:
			setting=get_setting(self.site_id,i.value);
			if setting:context[i.name]=setting;
		active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);parent_order=1;menu_footer0=get_menu_caches_footer2(self.request,f"header_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer0);parent_order=2;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=3;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);context[_u]=get_logo_pos(self.site_id,OptLogoSettingPos.TOP_NORMAL);context[_v]=get_logo_pos(self.site_id,OptLogoSettingPos.TOP_DARK);context[_w]=get_logo_pos(self.site_id,OptLogoSettingPos.BOTTOM_NORMAL);context[_x]=get_logo_pos(self.site_id,OptLogoSettingPos.BOTTOM_DARK);context[_y]=get_format_date();lang=get_active_language_choices()[0];context['banner']=get_banner(self.site_id);context[_C]=get_announcement(self.site_id,lang,max_data=10);context[_A8]=get_autoheadline(self.site_id,lang);context['article_notes']=get_article_notes(self.site_id,lang);context['flash_news']=get_flash_news(self.site_id,lang);context['popular']=get_popular(self.site_id,lang);context[_P]=get_slideshow(self.site_id,lang,max_data=10);context['dailyalert']=get_dailyalert(self.site_id,lang,max_data=10);context[_h]=get_howitworks(self.site_id,lang,max_data=10);context[_m]=get_aboutus(self.site_id,lang,max_data=5);context[_n]=get_testimony(self.site_id,lang,max_data=10);context[_a]=get_product(self.site_id,lang,max_data=10);context['whyus']=get_whyus(self.site_id,lang,max_data=10);context[_Y]=get_fasilities(self.site_id,lang);context[_Z]=get_offers(self.site_id,lang);context[_b]=get_greeting(self.site_id,lang);context[_Q]=get_events(self.site_id,lang);context[_L]=get_photogallery(self.site_id,lang);context[_A6]=get_videogallery(self.site_id,lang);context[_W]=get_relatedlink(self.site_id,lang);context[_E]=get_news(self.site_id,lang,max_data=10);context[_I]=get_article(self.site_id,lang,max_data=10);context[_i]=get_document(self.site_id,lang,max_data=10);context[_X]=get_socialmedia(self.site_id,max_data=10);context[_p]=get_location(self.site_id,lang);context[_N]=get_base_url(self.request);og=get_og(self.site_id);context.update(og);return context
class CheckOutView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_c%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'checkout.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		B='footer_menu_2';A='footer_menu_1';context=super().get_context_data(*(args),**kwargs);context[_g]='checkout';context[_M]=self.request.device[_M];active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);menu_footer1=get_menu_caches_footer(self.request,A,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=A);context.update(menu_footer1);menu_footer2=get_menu_caches_footer(self.request,B,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=B);context.update(menu_footer2);context[_d]=get_menu_group(self.site_id);slug=self.kwargs[_T]
		if not slug:raise Http404(_A0%(self.request.get_host(),_k))
		kind=self.kwargs[_J];context[_J]=kind;model=apps.get_model(_H,kind);agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);lang=get_active_language_choices()[0];content_detail=get_content_detail(self.site_id,lang,model,kind,slug);context[_A1]=content_detail;context[_W]=get_relatedlink(self.site_id,lang);context[_X]=get_socialmedia(self.site_id);context[_P]=get_slideshow(self.site_id,lang);context[_N]=get_base_url(self.request,1);return context
class DetailView(TemplateView):
	site_id=_A;count_hit=_G
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_c%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'detail.html';return super(DetailView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		B='random_paint_kind';A='latest_kind_kind';context=super(DetailView,self).get_context_data(*(args),**kwargs);context[_g]='detail';context[_M]=self.request.device[_M];active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);parent_order=1;menu_footer0=get_menu_caches_footer2(self.request,f"header_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer0);parent_order=2;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=3;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);context[_d]=get_menu_group(self.site_id);slug=self.kwargs[_T]
		if not slug:raise Http404(_A0%(self.request.get_host(),_k))
		agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);context[_u]=get_logo_pos(self.site_id,OptLogoSettingPos.TOP_NORMAL);context[_v]=get_logo_pos(self.site_id,OptLogoSettingPos.TOP_DARK);context[_w]=get_logo_pos(self.site_id,OptLogoSettingPos.BOTTOM_NORMAL);context[_x]=get_logo_pos(self.site_id,OptLogoSettingPos.BOTTOM_DARK);context[_y]=get_format_date();lang=get_active_language_choices()[0];model_with_categories=[_C,_E,_I,_Q,_i,_j];model_with_content=[_C,_E,_I,_Q,_P,_b,_j,_L,_Y,_Z,_h,_m,_n,_a,_i];model_randomize=[_E,_I,_Q,_Y,_Z,_h,_a,_j];kind=self.kwargs[_J];
		if kind in model_with_content:context[_J]=kind
		context[_C]=get_announcement(self.site_id,lang,6);model=apps.get_model(_H,kind);latest_kind=_A;random_paint=_A;
		if kind in model_with_categories:context[_A9]=get_categories_list(self.site_id,lang,10,model);context[_AA]=get_tags_list(self.site_id,lang,10,model);latest_kind=get_latest_model(self.site_id,lang,10,model,kind,slug);random_paint=get_related_model(self.site_id,lang,10,model,kind,slug)
		idx=0
		for i in model_randomize:
			if i==kind.lower():model_randomize.pop(idx);break
			idx+=1
		tmp_kind=_A
		if not latest_kind:
			random.shuffle(model_randomize)
			for i in model_randomize:
				tmp_kind=i;tmp_model=apps.get_model(_H,i);latest_kind=get_latest_model(self.site_id,lang,10,tmp_model,i)
				if latest_kind:break
		context[_AB]=latest_kind;context[A]=tmp_kind;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		if not random_paint:
			random.shuffle(model_randomize)
			for i in model_randomize:
				tmp_kind=i;tmp_model=apps.get_model(_H,i);random_paint=get_related_model(self.site_id,lang,4,tmp_model,i)
				if random_paint:break
		context[_AC]=random_paint;context[B]=tmp_kind;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		random_model=_A;random.shuffle(model_randomize)
		for i in model_randomize:
			tmp_model=apps.get_model(_H,i);random_model=get_model_content(self.site_id,lang,tmp_model,i,10)
			if random_model:break
		context[_AD]=random_model;content_detail=get_content_detail(self.site_id,lang,model,kind,slug);context[_A1]=content_detail;context[_L]=get_photogallery(self.site_id,lang);context[_W]=get_relatedlink(self.site_id,lang);context[_X]=get_socialmedia(self.site_id);context[_p]=get_location(self.site_id,lang);context[_P]=get_slideshow(self.site_id,lang);context[_N]=get_base_url(self.request,1);
		if not context[A]:context[A]=context[_J]
		if not context[B]:context[B]=context[_J]
		return context
class ListView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_c%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'list.html';return super(ListView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ListView,self).get_context_data(*(args),**kwargs);context[_g]='list';context[_M]=self.request.device[_M];active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);parent_order=1;menu_footer0=get_menu_caches_footer2(self.request,f"header_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer0);parent_order=2;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=3;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);context[_d]=get_menu_group(self.site_id);slug=self.kwargs[_T]
		if not slug:raise Http404(_A0%(self.request.get_host(),_k))
		agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);context[_u]=get_logo_pos(self.site_id,OptLogoSettingPos.TOP_NORMAL);context[_v]=get_logo_pos(self.site_id,OptLogoSettingPos.TOP_DARK);context[_w]=get_logo_pos(self.site_id,OptLogoSettingPos.BOTTOM_NORMAL);context[_x]=get_logo_pos(self.site_id,OptLogoSettingPos.BOTTOM_DARK);context[_y]=get_format_date();lang=get_active_language_choices()[0];model_with_categories=[_C,_E,_I,_Q,_i,_j];model_with_content=[_C,_E,_I,_Q,_P,_b,_j,_L,_Y,_Z,_h,_m,_n,_a,_i];model_randomize=[_E,_I,_Q,_Y,_Z,_h,_a];kind=self.kwargs[_J]
		if kind in model_with_content:context[_J]=kind
		else:raise Http404(_t)
		context[_C]=get_announcement(self.site_id,lang,6);model=apps.get_model(_H,kind);latest_kind=_A;random_paint=_A;
		if kind in model_with_categories:context[_A9]=get_categories_list(self.site_id,lang,10,model);context[_AA]=get_tags_list(self.site_id,lang,10,model);latest_kind=get_latest_model(self.site_id,lang,10,model,kind,slug);random_paint=get_related_model(self.site_id,lang,10,model,kind,slug)
		idx=0
		for i in model_randomize:
			if i==kind.lower():model_randomize.pop(idx);break
			idx+=1
		tmp_kind=_A
		if not latest_kind:
			random.shuffle(model_randomize)
			for i in model_randomize:
				tmp_kind=i;tmp_model=apps.get_model(_H,i);latest_kind=get_latest_model(self.site_id,lang,10,tmp_model,i)
				if latest_kind:break
		context[_AB]=latest_kind;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		if not random_paint:
			random.shuffle(model_randomize)
			for i in model_randomize:
				tmp_kind=i;tmp_model=apps.get_model(_H,i);random_paint=get_related_model(self.site_id,lang,4,tmp_model,i)
				if random_paint:break
		context[_AC]=random_paint;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		random_model=_A;random.shuffle(model_randomize)
		for i in model_randomize:
			tmp_model=apps.get_model(_H,i);random_model=get_model_content(self.site_id,lang,tmp_model,i,10)
			if random_model:break
		context[_AD]=random_model;content_list=get_content_list(self.site_id,lang,model,kind,slug)
		if content_list:kind_data_per_page=8;paginator=Paginator(content_list,kind_data_per_page);page_number=self.request.GET.get('page',1);context['page_list']=paginator.get_page(page_number)
		context[_L]=get_photogallery(self.site_id,lang);context[_W]=get_relatedlink(self.site_id,lang);context[_X]=get_socialmedia(self.site_id);context[_p]=get_location(self.site_id,lang);context[_N]=get_base_url(self.request,1);context[_P]=get_slideshow(self.site_id,lang);return context
class DescriptionView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_c%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'description.html';return super(DescriptionView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DescriptionView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,kinds=1);context.update(menu);context[_d]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_C]=get_announcement(self.site_id,lang,6);model=apps.get_model(_H,_C);context[_A2]=get_latest_model(self.site_id,lang,5,model,_C);model=apps.get_model(_H,_E);context[_A3]=get_latest_model(self.site_id,lang,5,model,_E);context[_L]=get_photogallery(self.site_id,lang);context[_W]=get_relatedlink(self.site_id,lang);context[_X]=get_socialmedia(self.site_id);context[_N]=get_base_url(self.request);return context
class GreetingView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_c%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,1);context.update(menu);context[_d]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_C]=get_announcement(self.site_id,lang,6);context[_b]=get_greeting(self.site_id,lang);model=apps.get_model(_H,_C);context[_A2]=get_latest_model(self.site_id,lang,5,model,_C);model=apps.get_model(_H,_E);context[_A3]=get_latest_model(self.site_id,lang,5,model,_E);context[_L]=get_photogallery(self.site_id,lang);context[_W]=get_relatedlink(self.site_id,lang);context[_X]=get_socialmedia(self.site_id);context[_N]=get_base_url(self.request);return context
class BookingView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_c%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+_q;return super(BookingView,self).get(request,*(args),**kwargs)
	def post(self,request,*args,**kwargs):
		C='timeZone';B='dateTime';A='-';self.site_id=get_site_id_front(request);context=self.get_context_data(**kwargs);site=Site.objects.filter(id=self.site_id)
		if not site:template=get_template(self.site_id);self.template_name=template+_q;return self.render_to_response(context)
		site_domain=site.get().domain;name=self.request.POST.get(_f,_A);email=self.request.POST.get('email',_A);date_from=self.request.POST.get('date_from',_A);date_to=self.request.POST.get('date_to',_A);guest=self.request.POST.get('guest',_A);children=self.request.POST.get('children',_A);date_from_=parse(date_from);date_to_=parse(date_to);timeZone=_A4;event_request_body={_r:{B:str(date_from_.year)+A+str(date_from_.month)+A+str(date_from_.day)+'T00:00:00Z',C:timeZone},'end':{B:str(date_to_.year)+A+str(date_to_.month)+A+str(date_to_.day)+'00:00:00Z',C:timeZone},'summary':'Booking From <b>narvikvilla.com</b>',_A5:name+' ['+email+'] Guest:'+guest+', Children:'+children,'status':'confirmed','transparency':'opaque','visibility':'public',_p:'Senggigi'};cal=GoogleCalendar.objects.filter(site=self.site_id)[:1]
		if not cal:template=get_template(self.site_id);self.template_name=template+_q;return self.render_to_response(context)
		cal=cal.get();CLIENT_SECRET_FILE=cal.file_path_doc.path;calendar_id=cal.calendar_id;API_NAME='calendar';API_VERSION='v3';SCOPES=['https://www.googleapis.com/auth/calendar'];service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES);response=service.events().insert(calendarId=calendar_id,sendNotifications=sendNotification,sendUpdates=sendUpdate,body=event_request_body).execute();update_calendar(site_domain,date_from_.month,date_to_.month);template=get_template(self.site_id);self.template_name=template+_q;return self.render_to_response(context)
	def get_context_data(self,*args,**kwargs):context=super(BookingView,self).get_context_data(*(args),**kwargs);context[_g]='detail';context[_M]=self.request.device[_M];active_page=get_translated_active_page(_U);menu=get_menu_caches(self.request,_V,self.site_id,active_page,1);context.update(menu);parent_order=1;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=2;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);context[_d]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);context[_O]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_P]=get_slideshow(self.site_id,lang);context[_C]=get_announcement(self.site_id,lang,6);context[_b]=get_greeting(self.site_id,lang);model=apps.get_model(_H,_C);context[_A2]=get_latest_model(self.site_id,lang,5,model,_C);model=apps.get_model(_H,_E);context[_A3]=get_latest_model(self.site_id,lang,5,model,_E);context[_A1]='Booking';context[_L]=get_photogallery(self.site_id,lang);context[_W]=get_relatedlink(self.site_id,lang);context[_X]=get_socialmedia(self.site_id);context[_N]=get_base_url(self.request);return context
def copy_image(file_path):media_root=settings.MEDIA_ROOT;source=file_path;res=os.path.splitext(source);destination=res[0]+'_copy'+res[1];shutil.copy(os.path.join(media_root,source),os.path.join(media_root,destination));return destination
def get_autoheadline(site_id,lang):
	model_name='Auto Headline';is_refresh=_B;initial_date=timezone.now();expired_in=1;most_view_within=7;max_data=15;model_list=ModelList.objects.filter(name=model_name)[:1]
	if model_list:model_list=model_list[0]
	else:raise Http404("Model List '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(model_name,_R))
	tmp_log=Log.objects.filter(site_id=site_id,model_list=model_list)
	if not tmp_log:is_refresh=_G;Log.objects.create(site_id=site_id,model_list=model_list,expired=initial_date+datetime.timedelta(days=expired_in))
	else:
		is_refresh=tmp_log[0].is_need_refresh
		if is_refresh:post=tmp_log[0];post.is_need_refresh=_B;post.save()
	if not is_refresh:
		if tmp_log:
			tmp_expired=tmp_log[0].expired;tmp_diff=(tmp_expired-initial_date).days;
			if tmp_diff<0:is_refresh=_G;post=tmp_log[0];post.expired=initial_date+datetime.timedelta(days=expired_in);post.save()
	if is_refresh:
		AutoHeadline.objects.filter(site_id=site_id,is_editable=_G).delete();count_days=timezone.now()-datetime.timedelta(days=most_view_within);count_days=count_days.replace(hour=0,minute=0,second=0,microsecond=0);subquery_foto=get_photo(_C);obj_announcement=Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B,created_at__gte=count_days).annotate(file_path=subquery_foto)[:3]
		for i in obj_announcement:
			obj=AutoHeadline.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.ANNOUNCEMENT,is_editable=_G,created_at=i.created_at)
			if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj,file_path=destination)
			max_data-=1
		subquery_foto=get_photo(_I);obj_article=Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B,created_at__gte=count_days).annotate(file_path=subquery_foto)[:5];
		for i in obj_article:
			obj=AutoHeadline.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.ARTICLE,is_editable=_G,created_at=i.created_at)
			if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj,file_path=destination)
			max_data-=1
		subquery_foto=get_photo(_E);obj_news=News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B,created_at__gte=count_days).annotate(file_path=subquery_foto)[:10];
		for i in obj_news:
			obj=AutoHeadline.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.NEWS,is_editable=_G,created_at=i.created_at)
			if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj,file_path=destination)
			max_data-=1
			if max_data<=0:break
	subquery_foto=get_photo(_A8);obj=AutoHeadline.objects.filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_J,_K)
	for i in obj:i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_article_notes(site_id,lang):
	subquery_foto=get_photo(_I);obj=Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto).order_by(_K)[:5]
	for i in obj:i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_flash_news(site_id,lang):
	max_data=6;AutoFlashNews.objects.all().delete();subquery_foto=get_photo(_C);obj=Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto)[:1]
	for i in obj:
		obj_1=AutoFlashNews.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.ANNOUNCEMENT,is_editable=_G,created_at=i.created_at)
		if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj_1,file_path=destination)
		max_data-=1
	subquery_foto=get_photo(_I);obj=Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto)[:2]
	for i in obj:
		obj_1=AutoFlashNews.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.ARTICLE,is_editable=_G,created_at=i.created_at)
		if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj_1,file_path=destination)
		max_data-=1
	subquery_foto=get_photo(_E);obj=News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto)[:max_data]
	for i in obj:
		obj_1=AutoFlashNews.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.NEWS,is_editable=_G,created_at=i.created_at)
		if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj_1,file_path=destination)
	subquery_foto=get_photo('autoflashnews');obj=AutoFlashNews.objects.filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_J,_K)
	for i in obj:i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_popular(site_id,lang):
	A='view_count';max_data=8;AutoPopular.objects.all().delete();subquery_foto=get_photo(_C);obj=Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto).order_by(_K,A)[:1]
	for i in obj:
		obj_1=AutoPopular.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.ANNOUNCEMENT,is_editable=_G,created_at=i.created_at)
		if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj_1,file_path=destination)
		max_data-=1
	subquery_foto=get_photo(_I);obj=Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto).order_by(_K,A)[:2]
	for i in obj:
		obj_1=AutoPopular.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.ARTICLE,is_editable=_G,created_at=i.created_at)
		if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj_1,file_path=destination)
		max_data-=1
	subquery_foto=get_photo(_E);obj=News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED,is_header_text=_B).annotate(file_path=subquery_foto).order_by(_K,A)[:max_data]
	for i in obj:
		obj_1=AutoPopular.objects.create(site_id=site_id,admin_id=i.admin_id,title=i.title,sub_title=i.sub_title,slug=i.slug,categories=i.categories,kind=OptModelKinds.NEWS,is_editable=_G,created_at=i.created_at)
		if i.file_path:destination=copy_image(i.file_path);Photo.objects.create(content_object=obj_1,file_path=destination)
	subquery_foto=get_photo('autopopular');obj=AutoPopular.objects.filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_J,_K)
	for i in obj:i.created_at=get_natural_datetime(i.created_at)
	return obj