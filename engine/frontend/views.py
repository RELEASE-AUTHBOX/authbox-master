_A5='random_model'
_A4='random_paint'
_A3='latest_kind'
_A2='tags_list'
_A1='categories_list'
_A0='translations__name'
_z='videogallery'
_y='banner'
_x='Asia/Makassar'
_w='latest_news'
_v='latest_announcement'
_u='content_detail'
_t="Menu Group '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_s='baseurl'
_r='Halaman tidak ditemukan!'
_q='all'
_p='start'
_o='booking.html'
_n='location'
_m='count'
_l='testimony'
_k='aboutus'
_j='name'
_i='/dashboard'
_h='pages'
_g='document'
_f='howitworks'
_e='pagetype'
_d=True
_c='proses'
_b='menugroup'
_a="service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_Z='greeting'
_Y='product'
_X='offers'
_W='fasilities'
_V='socialmedia'
_U='relatedlink'
_T='menu'
_S='home'
_R='/admin'
_Q='slug'
_P='order_item'
_O='article'
_N='events'
_M='slideshow'
_L='logo'
_K=False
_J='kind'
_I='base_url'
_H='is_mobile'
_G='photogallery'
_F='news'
_E='frontend'
_D='announcement'
_C='-updated_at'
_B='-is_header_text'
_A=None
import calendar,datetime,random
from dateutil.parser import parse
from django_authbox.common import get_natural_datetime
from django.shortcuts import redirect
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Count,OuterRef,Subquery
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
	print('get_calendar_ajax - request',request);site_id=get_site_id_front(request);res=[];calendar_id=get_calendar_id(site_id);print('calendar_id',calendar_id);timeZone=_x;bg_color=['rgb(220, 235, 252)','rgb(173, 209, 245)','rgb(129, 180, 237)','rgb(38, 101, 167)','rgb(0, 116, 217)'];bg_cal_name=[];TZA=pytz.timezone(timeZone);res=[];gc=GoogleCalendar.objects.filter(calendar_id=calendar_id)[:1]
	if gc:
		gcd=GoogleCalendarDetail.objects.filter(cal_year=year,cal_month=month,site_id=site_id,google_calendar=gc).order_by(_p)
		for i in gcd:
			if i.cal_name not in bg_cal_name:bg_cal_name.append(i.cal_name)
			tmp_color=-1
			for (j,name) in enumerate(bg_cal_name):
				if name==i.cal_name:tmp_color=j
			if tmp_color>=len(bg_color):tmp_color=-1
			tmp={'title':i.summary,_p:i.start.astimezone(TZA).isoformat(),'end':i.end.astimezone(TZA).isoformat(),'desc':i.description,'eventBackgroundColor':''if tmp_color<0 else bg_color[tmp_color]};res.append(tmp)
	return JsonResponse(res,safe=_K)
def get_menu_group(site_id):
	menugroup=MenuGroup.objects.filter(site_id=site_id,kind=1)
	if menugroup:return menugroup[0].id
	else:raise Http404("Menu Group belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_i)
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=model_name).values('file_path')[:1])
def get_logo(site_id,max_data=1):
	subquery_foto=get_photo(_L);logo=Logo.objects.filter(site_id=site_id).values(_j).annotate(file_path=subquery_foto)[:max_data]
	if logo:return logo
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
def get_statistic(site_id,is_cache=_K):
	C='user_agent';B=')';A='load from DB (';context={};tgl=datetime.datetime.now();content_type_id=ContentType.objects.get(app_label='sites',model='site');content_type_id=content_type_id.id if content_type_id else _A;hitcount_id=HitCount.objects.filter(content_type_id=content_type_id,object_pk=site_id).first();hitcount_id=hitcount_id.id if hitcount_id else _A;tgl00=tgl+datetime.timedelta(days=1);jam00=datetime.datetime(tgl00.year,tgl00.month,tgl00.day,0,1,0);timeout=(jam00-tgl00).seconds;selisih=0;tmp='hit_today';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);hit_today=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day);tmp_cache=hit_today.count()if hit_today else 1;cache.set(tmp,tmp_cache,timeout,version=site_id);context[tmp]=tmp_cache
	else:hit_today=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month,created__day=tgl.day);context[tmp]=hit_today.count()if hit_today else 1;selisih=context[tmp]-tmp_cache;print('selisih = ',selisih)
	tmp='hit_yesterday';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);start_date=tgl+datetime.timedelta(days=-1);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=start_date.year,created__month=start_date.month,created__day=start_date.day).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;tmp='hit_this_week';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);start_date,end_date=get_week_date(tgl.year,tgl.month,tgl.day);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;tmp='hit_last_week';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);start_date,end_date=get_week_date(tgl.year,tgl.month,tgl.day);start_date=start_date+datetime.timedelta(days=-7);end_date=end_date+datetime.timedelta(days=-7);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;tmp='hit_this_month';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=tgl.year,created__month=tgl.month).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;tmp='hit_last_month';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);start_date=add_months(tgl,-1);tmp_cache=Hit.objects.filter(hitcount_id=hitcount_id,created__year=start_date.year,created__month=start_date.month).count();cache.set(tmp,tmp_cache,timeout,version=site_id)
	context[tmp]=tmp_cache;start_date=tgl+datetime.timedelta(hours=-5);start_date=datetime.datetime(start_date.year,start_date.month,start_date.day,start_date.hour,0,0);end_date=datetime.datetime(tgl.year,tgl.month,tgl.day,tgl.hour,59,59);hit_online=Hit.objects.filter(hitcount_id=hitcount_id,created__range=(start_date,end_date)).values(C).order_by(C).distinct();context['hit_online']=hit_online.count()if hit_online else 1;tmp='hit_all';tmp_cache=cache.get(tmp,version=site_id)
	if not(is_cache and tmp_cache is not _A):print(A+tmp+B);hit_count=HitCount.objects.filter(object_pk=site_id,content_type_id=content_type_id);tmp_cache=hit_count[0].hits if hit_count else 1;cache.set(tmp,tmp_cache,timeout,version=site_id)
	tmp_cache+=selisih;context[tmp]=tmp_cache;return context
def get_model_content(site_id,lang,model,kind,max_data):
	subquery_foto=get_photo(kind);obj=model.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
	for i in obj:i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_banner(site_id,max_data=3):subquery_foto=get_photo(_y);return Banner.objects.filter(site_id=site_id).annotate(file_path=subquery_foto)[:max_data]
def get_announcement(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_D);obj=Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by('priority',_C)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_slideshow(site_id,lang,max_data=5,is_random=_K):
	subquery_foto=get_photo(_M);obj=SlideShow.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:max_data]
	if is_random:obj=list(obj);random.shuffle(obj)
	return obj
def get_fasilities(site_id,lang,exclude_id=[],is_header_text=_A,is_shuffle=_A):
	print('exclude_id',exclude_id);subquery_foto=get_photo(_W)
	if is_header_text is _A:print('isheadertext1',is_header_text);obj=Fasilities.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).annotate(file_path=subquery_foto).order_by(_B,_P)[:10];print(obj)
	else:print('isheadertext2',is_header_text);obj=Fasilities.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).exclude(is_header_text=is_header_text).annotate(file_path=subquery_foto).order_by(_B,_P)[:10]
	obj=list(obj)
	if is_shuffle:random.shuffle(obj)
	return obj
def get_offers(site_id,lang,exclude_id=[],is_header_text=_A,is_shuffle=_A):
	subquery_foto=get_photo(_X)
	if is_header_text is _A:obj=Offers.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).annotate(file_path=subquery_foto).order_by(_B,_P)[:10]
	else:obj=Offers.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).exclude(is_header_text=_d).annotate(file_path=subquery_foto).order_by(_B,_P)[:10]
	return obj
def get_whyus(site_id,lang,max_data=3):return WhyUs.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_B,_C)[:max_data]
def get_dailyalert(site_id,lang,max_data=3):return DailyAlert.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:max_data]
def get_howitworks(site_id,lang,max_data=3,max_words=20):
	obj=HowItWorks.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_B,_P)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_aboutus(site_id,lang,max_data=1,max_words=100):subquery_foto=get_photo(_k);obj=AboutUs.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by('id')[:max_data];return obj
def get_testimony(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_l);obj=Testimony.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_product(site_id,lang,max_data=3,max_words=20):subquery_foto=get_photo(_Y);obj=Product.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_P)[:max_data];return obj
def get_greeting(site_id,lang,max_data=1):subquery_foto=get_photo(_Z);return Greeting.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:max_data]
def get_events(site_id,lang,max_data=3):subquery_foto=get_photo(_N);return Events.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
def get_photogallery(site_id,lang,max_data=16):subquery_foto=get_photo(_G);return PhotoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_P)[:max_data]
def get_videogallery(site_id,lang,max_data=16):subquery_foto=get_photo(_z);return VideoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
def get_relatedlink(site_id,lang,max_data=3):return RelatedLink.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:max_data]
def get_news(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_F);obj=News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_article(site_id,lang,max_data=3,max_words=20):
	subquery_foto=get_photo(_O);obj=Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_document(site_id,lang,max_data=3,max_words=20):
	obj=Document.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_B,_C)[:max_data]
	for i in obj:
		if not i.is_header_text:i.content=Truncator(strip_tags(i.content)).words(max_words);i.created_at=get_natural_datetime(i.created_at)
	return obj
def get_socialmedia(site_id,max_data=5):return SocialMedia.objects.filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:max_data]
def get_categories_list(site_id,lang,max_data,model):
	A='categories_id';subquery=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values(_A0)[:1]);subquery_slug=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values(_Q)[:1]);categories_list=[];obj=model.objects.filter(site_id=site_id).values(A).annotate(count=Count(A)).annotate(name=subquery).annotate(slug=subquery_slug).order_by(A)[:max_data]
	if obj:
		all_data=0
		for i in obj:all_data+=i[_m]
		categories_list=list(obj);categories_all={A:0,_m:all_data,_j:'All',_Q:_q};categories_list.insert(0,categories_all);return categories_list
def get_tags_list(site_id,lang,max_data,model):
	site_name={f"{model.__name__.lower()}__site":f"{site_id}"};val=f"{model.__name__.lower()}__tags";subquery=Subquery(Tags.objects.translated(lang).filter(id=OuterRef(val)).values(_A0)[:1]);subquery_slug=Subquery(Tags.objects.translated(lang).filter(id=OuterRef(val)).values(_Q)[:1]);tags_list=[];obj=model.tags.through.objects.filter(**site_name).values(val).annotate(count=Count(val)).annotate(name=subquery).annotate(slug=subquery_slug).order_by(val)[:max_data]
	if obj:
		all_data=0
		for i in obj:all_data+=i[_m]
		tags_list=list(obj);tags_all={'tags_id':0,_m:all_data,_j:'All',_Q:_q};tags_list.insert(0,tags_all);return tags_list
def get_latest_model(site_id,lang,max_data,model,kind,exclude_slug=_A):
	subquery_foto=get_photo(kind)
	if exclude_slug:return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).exclude(slug=exclude_slug).order_by(_B,_C)[:max_data]
	return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_B,_C)[:max_data]
def get_random_items(qs,max_data):possible_ids=list(qs.values_list('id',flat=_d));req_no_of_random_items=len(possible_ids)+1 if len(possible_ids)+1<max_data else max_data;possible_ids=random.choices(possible_ids,k=req_no_of_random_items);return qs.filter(pk__in=possible_ids)
def get_related_model(site_id,lang,max_data,model,kind,exclude_slug=_A):
	subquery_foto=get_photo(kind)
	if exclude_slug:qs=model.objects.translated(lang).filter(site_id=site_id,is_header_text=_K).exclude(slug=exclude_slug)
	else:qs=model.objects.translated(lang).filter(site_id=site_id,is_header_text=_K)
	if qs:random_paint=get_random_items(qs,max_data);random_paint=random_paint.annotate(file_path=subquery_foto);header_text=model.objects.translated(lang).filter(site_id=site_id,is_header_text=_d).annotate(file_path=subquery_foto);return (header_text|random_paint).order_by(_B)
def get_content_detail(site_id,lang,model,kind,slug):
	subquery_foto=get_photo(kind);obj=model.objects.translated(lang).filter(site_id=site_id,slug=slug).annotate(file_path=subquery_foto)
	if obj:obj=obj.get();obj.created_at=get_natural_datetime(obj.created_at);return obj
	raise Http404(_r)
def get_content_list(site_id,lang,model,kind,slug):
	A='-created_at'
	if not slug:raise Http404(_r)
	field_is_header_text_exists=_K
	for field in model._meta.get_fields():
		if field.name=='is_header_text':field_is_header_text_exists=_d;break
	subquery_foto=get_photo(kind)
	if slug==_q:
		if field_is_header_text_exists:return model.objects.translated(lang).filter(site_id=site_id,is_header_text=_K).annotate(file_path=subquery_foto).order_by(A)
		return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(A)
	else:
		categories=Categories.objects.filter(slug=slug);categories=categories.get()if categories else _A
		if categories:
			if field_is_header_text_exists:return model.objects.translated(lang).filter(site_id=site_id,categories_id=categories.id,is_header_text=_K).annotate(file_path=subquery_foto).order_by(A)
			return model.objects.translated(lang).filter(site_id=site_id,categories_id=categories.id).annotate(file_path=subquery_foto).order_by(A)
		raise Http404('Categories '+slug+' tidak ditemukan!')
def get_location(site_id,lang,max_data=2):return Location.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_B,_C)[:max_data]
def get_og(site_id):
	ret={};ret['og_type']='website';site=Site.objects.get(id=site_id)
	if site:ret['og_url']=site.domain
	return ret
def set_setting(site_id,setting_id):
	B='model list';A='label =';template_id=get_template_id(site_id);template=get_template(site_id);template_block=TemplateBlock.objects.filter(template_id=template_id,price_level=1,status=OptStatusPublish.PUBLISHED);print('template block',template_block);label=''
	for i in OptSettingName:
		print('--->',i.value,setting_id)
		if i.value==setting_id:label=i.label;break
	print(A,type(label));print(A,str(label));ret=_A
	for i in template_block:
		print(B,i.model_list.all());print(B,[j.name for j in i.model_list.all()])
		if str(label)in[j.name for j in i.model_list.all()]:print('ENTER0000',str(label));ret=template+i.name;GlobalSetting.objects.create(site_id=site_id,name=setting_id,value=ret,ref_template_block_id=i.id);break
	return ret
def get_setting(site_id,setting_id):
	global_setting=GlobalSetting.objects.filter(site_id=site_id,name=setting_id);print('global setting',global_setting)
	if global_setting:return global_setting[0].value
	return set_setting(site_id,setting_id)
class IndexView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		hostname=request.get_host();hostname_split=hostname.strip().split('.')
		if hostname_split[0]=='www':hostname_split.pop(0);hostname='.'.join(hostname_split);return redirect(f"https://{hostname}")
		service=service_exists(request);print('service from index',service);service_type=service;print('servicetype',service_type)
		if not service_type:raise Http404("service belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_R)
		self.site_id=get_site_id_front(request)
		if request.session.session_key:obj=Site.objects.get(id=self.site_id)
		template=get_template(self.site_id);print('template=',template);self.template_name=template+'index.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super().get_context_data(*(args),**kwargs);context[_e]='index';context['menu_justify']='right';context['agency_meta']=get_agency_meta(self.request,self.site_id);context[_H]=self.request.device[_H];print('OptSettingName',OptSettingName)
		for i in OptSettingName:
			print('call get setting',self.site_id,i.value);setting=get_setting(self.site_id,i.value);print('setting ADALAH',setting)
			if setting:context[i.name]=setting;print('result',i.name,setting)
		active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);parent_order=1;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=2;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);print('menu_footer1=',menu_footer1);print('menu_footer2=',menu_footer2);agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_y]=get_banner(self.site_id);context[_D]=get_announcement(self.site_id,lang,max_data=10);context[_M]=get_slideshow(self.site_id,lang,max_data=10);context['dailyalert']=get_dailyalert(self.site_id,lang,max_data=10);context[_f]=get_howitworks(self.site_id,lang,max_data=10);context[_k]=get_aboutus(self.site_id,lang,max_data=5);context[_l]=get_testimony(self.site_id,lang,max_data=10);context[_Y]=get_product(self.site_id,lang,max_data=10);context['whyus']=get_whyus(self.site_id,lang,max_data=10);context[_W]=get_fasilities(self.site_id,lang);context[_X]=get_offers(self.site_id,lang);context[_Z]=get_greeting(self.site_id,lang);context[_N]=get_events(self.site_id,lang);context[_G]=get_photogallery(self.site_id,lang);print('!!! photo gallery !!! ====',context[_G]);context[_z]=get_videogallery(self.site_id,lang);context[_U]=get_relatedlink(self.site_id,lang);context[_F]=get_news(self.site_id,lang,max_data=10);context[_O]=get_article(self.site_id,lang,max_data=10);context[_g]=get_document(self.site_id,lang,max_data=10);context[_V]=get_socialmedia(self.site_id,max_data=10);context[_n]=get_location(self.site_id,lang);context[_I]=get_base_url(self.request);print(_s,context[_I]);og=get_og(self.site_id);context.update(og);return context
class CheckOutView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_a%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'checkout.html';return super().get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		B='footer_menu_2';A='footer_menu_1';context=super().get_context_data(*(args),**kwargs);context[_e]='checkout';context[_H]=self.request.device[_H];active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);menu_footer1=get_menu_caches_footer(self.request,A,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=A);context.update(menu_footer1);menu_footer2=get_menu_caches_footer(self.request,B,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=B);context.update(menu_footer2);context[_b]=get_menu_group(self.site_id);slug=self.kwargs[_Q]
		if not slug:raise Http404(_t%(self.request.get_host(),_i))
		kind=self.kwargs[_J];context[_J]=kind;model=apps.get_model(_E,kind);agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];content_detail=get_content_detail(self.site_id,lang,model,kind,slug);context[_u]=content_detail;context[_U]=get_relatedlink(self.site_id,lang);context[_V]=get_socialmedia(self.site_id);context[_M]=get_slideshow(self.site_id,lang);context[_I]=get_base_url(self.request,1);print(_s,context[_I]);return context
class DetailView(TemplateView):
	site_id=_A;count_hit=_d
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_a%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'detail.html';return super(DetailView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		B='random_paint_kind';A='latest_kind_kind';context=super(DetailView,self).get_context_data(*(args),**kwargs);context[_e]='detail';context[_H]=self.request.device[_H];active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);parent_order=1;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=2;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);context[_b]=get_menu_group(self.site_id);slug=self.kwargs[_Q]
		if not slug:raise Http404(_t%(self.request.get_host(),_i))
		agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];model_with_categories=[_D,_F,_O,_N,_g,_h];model_with_content=[_D,_F,_O,_N,_M,_Z,_h,_G,_W,_X,_f,_k,_l,_Y,_g];model_randomize=[_F,_O,_N,_W,_X,_f,_Y,_h];kind=self.kwargs[_J];print('kind detail',kind)
		if kind in model_with_content:context[_J]=kind
		context[_D]=get_announcement(self.site_id,lang,6);model=apps.get_model(_E,kind);latest_kind=_A;random_paint=_A;print('1',model_randomize)
		if kind in model_with_categories:context[_A1]=get_categories_list(self.site_id,lang,10,model);context[_A2]=get_tags_list(self.site_id,lang,10,model);latest_kind=get_latest_model(self.site_id,lang,10,model,kind,slug);random_paint=get_related_model(self.site_id,lang,10,model,kind,slug)
		print(_J,kind);idx=0
		for i in model_randomize:
			if i==kind.lower():model_randomize.pop(idx);break
			idx+=1
		print('2',model_randomize);tmp_kind=_A
		if not latest_kind:
			random.shuffle(model_randomize)
			for i in model_randomize:
				print(_c,i);tmp_kind=i;tmp_model=apps.get_model(_E,i);latest_kind=get_latest_model(self.site_id,lang,10,tmp_model,i)
				if latest_kind:break
		context[_A3]=latest_kind;context[A]=tmp_kind;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		print('3',model_randomize)
		if not random_paint:
			random.shuffle(model_randomize)
			for i in model_randomize:
				print(_c,i);tmp_kind=i;tmp_model=apps.get_model(_E,i);random_paint=get_related_model(self.site_id,lang,4,tmp_model,i)
				if random_paint:break
		context[_A4]=random_paint;context[B]=tmp_kind;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		print('4',model_randomize);random_model=_A;random.shuffle(model_randomize)
		for i in model_randomize:
			print(_c,i);tmp_model=apps.get_model(_E,i);random_model=get_model_content(self.site_id,lang,tmp_model,i,10)
			if random_model:break
		context[_A5]=random_model;content_detail=get_content_detail(self.site_id,lang,model,kind,slug);context[_u]=content_detail;context[_G]=get_photogallery(self.site_id,lang);context[_U]=get_relatedlink(self.site_id,lang);context[_V]=get_socialmedia(self.site_id);context[_n]=get_location(self.site_id,lang);context[_M]=get_slideshow(self.site_id,lang);context[_I]=get_base_url(self.request,1);print(_s,context[_I])
		if not context[A]:context[A]=context[_J]
		if not context[B]:context[B]=context[_J]
		return context
class ListView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_a%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'list.html';return super(ListView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ListView,self).get_context_data(*(args),**kwargs);print('enter list view');context[_e]='list';context[_H]=self.request.device[_H];active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);parent_order=1;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=2;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);context[_b]=get_menu_group(self.site_id);slug=self.kwargs[_Q]
		if not slug:raise Http404(_t%(self.request.get_host(),_i))
		agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];model_with_categories=[_D,_F,_O,_N,_g,_h];model_with_content=[_D,_F,_O,_N,_M,_Z,_h,_G,_W,_X,_f,_k,_l,_Y,_g];model_randomize=[_F,_O,_N,_W,_X,_f,_Y];kind=self.kwargs[_J]
		if kind in model_with_content:context[_J]=kind
		else:raise Http404(_r)
		print('Kind = ',kind);context[_D]=get_announcement(self.site_id,lang,6);model=apps.get_model(_E,kind);latest_kind=_A;random_paint=_A;print('1',model_randomize)
		if kind in model_with_categories:context[_A1]=get_categories_list(self.site_id,lang,10,model);context[_A2]=get_tags_list(self.site_id,lang,10,model);latest_kind=get_latest_model(self.site_id,lang,10,model,kind,slug);random_paint=get_related_model(self.site_id,lang,10,model,kind,slug)
		print('detail model = ',model,kind);print(_J,kind);idx=0
		for i in model_randomize:
			if i==kind.lower():model_randomize.pop(idx);break
			idx+=1
		print('2',model_randomize);tmp_kind=_A
		if not latest_kind:
			random.shuffle(model_randomize)
			for i in model_randomize:
				print(_c,i);tmp_kind=i;tmp_model=apps.get_model(_E,i);latest_kind=get_latest_model(self.site_id,lang,10,tmp_model,i)
				if latest_kind:break
		context[_A3]=latest_kind;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		print('3',model_randomize)
		if not random_paint:
			random.shuffle(model_randomize)
			for i in model_randomize:
				print(_c,i);tmp_kind=i;tmp_model=apps.get_model(_E,i);random_paint=get_related_model(self.site_id,lang,4,tmp_model,i)
				if random_paint:break
		context[_A4]=random_paint;idx=0
		for i in model_randomize:
			if i==tmp_kind:model_randomize.pop(idx);break
			idx+=1
		print('4',model_randomize);random_model=_A;random.shuffle(model_randomize)
		for i in model_randomize:
			print(_c,i);tmp_model=apps.get_model(_E,i);random_model=get_model_content(self.site_id,lang,tmp_model,i,10)
			if random_model:break
		context[_A5]=random_model;content_list=get_content_list(self.site_id,lang,model,kind,slug)
		if content_list:kind_data_per_page=8;paginator=Paginator(content_list,kind_data_per_page);page_number=self.request.GET.get('page',1);context['page_list']=paginator.get_page(page_number)
		context[_G]=get_photogallery(self.site_id,lang);context[_U]=get_relatedlink(self.site_id,lang);context[_V]=get_socialmedia(self.site_id);context[_n]=get_location(self.site_id,lang);context[_I]=get_base_url(self.request,1);context[_M]=get_slideshow(self.site_id,lang);return context
class DescriptionView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_a%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'description.html';return super(DescriptionView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DescriptionView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,kinds=1);context.update(menu);context[_b]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_D]=get_announcement(self.site_id,lang,6);model=apps.get_model(_E,_D);context[_v]=get_latest_model(self.site_id,lang,5,model,_D);model=apps.get_model(_E,_F);context[_w]=get_latest_model(self.site_id,lang,5,model,_F);context[_G]=get_photogallery(self.site_id,lang);context[_U]=get_relatedlink(self.site_id,lang);context[_V]=get_socialmedia(self.site_id);context[_I]=get_base_url(self.request);return context
class GreetingView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_a%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,1);context.update(menu);context[_b]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_D]=get_announcement(self.site_id,lang,6);context[_Z]=get_greeting(self.site_id,lang);model=apps.get_model(_E,_D);context[_v]=get_latest_model(self.site_id,lang,5,model,_D);model=apps.get_model(_E,_F);context[_w]=get_latest_model(self.site_id,lang,5,model,_F);context[_G]=get_photogallery(self.site_id,lang);context[_U]=get_relatedlink(self.site_id,lang);context[_V]=get_socialmedia(self.site_id);context[_I]=get_base_url(self.request);return context
class BookingView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_a%(request.get_host(),_R))
		template=get_template(self.site_id);self.template_name=template+_o;return super(BookingView,self).get(request,*(args),**kwargs)
	def post(self,request,*args,**kwargs):
		C='timeZone';B='dateTime';A='-';self.site_id=get_site_id_front(request);context=self.get_context_data(**kwargs);print('site_ids',self.site_id);site=Site.objects.filter(id=self.site_id)
		if not site:print('Site Not Found!');template=get_template(self.site_id);self.template_name=template+_o;return self.render_to_response(context)
		site_domain=site.get().domain;print('site_domain',site_domain);name=self.request.POST.get(_j,_A);email=self.request.POST.get('email',_A);date_from=self.request.POST.get('date_from',_A);date_to=self.request.POST.get('date_to',_A);guest=self.request.POST.get('guest',_A);children=self.request.POST.get('children',_A);date_from_=parse(date_from);date_to_=parse(date_to);timeZone=_x;event_request_body={_p:{B:str(date_from_.year)+A+str(date_from_.month)+A+str(date_from_.day)+'T00:00:00Z',C:timeZone},'end':{B:str(date_to_.year)+A+str(date_to_.month)+A+str(date_to_.day)+'00:00:00Z',C:timeZone},'summary':'Booking From <b>narvikvilla.com</b>','description':name+' ['+email+'] Guest:'+guest+', Children:'+children,'status':'confirmed','transparency':'opaque','visibility':'public',_n:'Senggigi'};cal=GoogleCalendar.objects.filter(site=self.site_id)[:1]
		if not cal:print('Calendar Not Found!');template=get_template(self.site_id);self.template_name=template+_o;return self.render_to_response(context)
		cal=cal.get();CLIENT_SECRET_FILE=cal.file_path_doc.path;calendar_id=cal.calendar_id;API_NAME='calendar';API_VERSION='v3';SCOPES=['https://www.googleapis.com/auth/calendar'];service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES);response=service.events().insert(calendarId=calendar_id,sendNotifications=sendNotification,sendUpdates=sendUpdate,body=event_request_body).execute();update_calendar(site_domain,date_from_.month,date_to_.month);template=get_template(self.site_id);self.template_name=template+_o;return self.render_to_response(context)
	def get_context_data(self,*args,**kwargs):context=super(BookingView,self).get_context_data(*(args),**kwargs);context[_e]='detail';context[_H]=self.request.device[_H];active_page=get_translated_active_page(_S);menu=get_menu_caches(self.request,_T,self.site_id,active_page,1);context.update(menu);parent_order=1;menu_footer1=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer1);parent_order=2;menu_footer2=get_menu_caches_footer2(self.request,f"footer_menu_{parent_order}",self.site_id,active_page,kinds=1,exclude_menu=1,parent_order=parent_order);context.update(menu_footer2);context[_b]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);context[_L]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_M]=get_slideshow(self.site_id,lang);context[_D]=get_announcement(self.site_id,lang,6);context[_Z]=get_greeting(self.site_id,lang);model=apps.get_model(_E,_D);context[_v]=get_latest_model(self.site_id,lang,5,model,_D);model=apps.get_model(_E,_F);context[_w]=get_latest_model(self.site_id,lang,5,model,_F);context[_u]='Booking';context[_G]=get_photogallery(self.site_id,lang);context[_U]=get_relatedlink(self.site_id,lang);context[_V]=get_socialmedia(self.site_id);context[_I]=get_base_url(self.request);return context