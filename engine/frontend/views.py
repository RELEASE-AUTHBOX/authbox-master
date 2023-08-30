_w='random_paint'
_v='latest_kind'
_u="Menu Group '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_t='translations__name'
_s='product'
_r='testimony'
_q='aboutus'
_p='banner'
_o='latest_news'
_n='latest_announcement'
_m='categories_list'
_l='document'
_k='footer_menu_2'
_j='menu_footer2'
_i='footer_menu_1'
_h='menu_footer1'
_g='all'
_f='name'
_e='/dashboard'
_d='kind'
_c='pages'
_b='Halaman tidak ditemukan!'
_a='count'
_Z='article'
_Y='videogallery'
_X='events'
_W='menugroup'
_V="service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_U='offers'
_T='fasilities'
_S='base_url'
_R='socialmedia'
_Q='relatedlink'
_P='menu'
_O='home'
_N='/admin'
_M='slug'
_L='slideshow'
_K='order_item'
_J='logo'
_I='frontend'
_H='greeting'
_G='photogallery'
_F='news'
_E=True
_D='-is_header_text'
_C='-updated_at'
_B='announcement'
_A=None
import calendar,datetime,random
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
from backend.views import get_menu_caches,get_translated_active_page,get_menu_caches_footer
from core.common import get_agency_info
from core.models import Agency,Service
from django_authbox.common import add_months,get_site_id_front,get_template,get_week_date
from django_authbox.views import service_exists
from .calendar import sync_calendar_all
from .models import *
def get_calendar_ajax(request,year,month):A='get_calendar_ajax';print(A,request);print(A,year,month);res=sync_calendar_all(request,year,month);return JsonResponse(res,safe=False)
def get_menu_group(site_id):
	menugroup=MenuGroup.objects.filter(site_id=site_id,kind=1)
	if menugroup:return menugroup[0].id
	else:raise Http404("Menu Group belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_e)
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=model_name).values('file_path')[:1])
def get_logo(site_id):
	subquery_foto=get_photo(_J);logo=Logo.objects.filter(site_id=site_id).values(_f).annotate(file_path=subquery_foto)[:1]
	if logo:return logo
def get_base_url(request):
	A='/';my_path=request.path.split(A)
	if my_path:
		if len(my_path)>2:return my_path[0]+A+my_path[1]+A+my_path[2]
def add_months(sourcedate,months):month=sourcedate.month-1+months;year=sourcedate.year+month//12;month=month%12+1;day=min(sourcedate.day,calendar.monthrange(year,month)[1]);return datetime.date(year,month,day)
def get_statistic(site_id,is_cache=False):
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
def get_banner(site_id):subquery_foto=get_photo(_p);return Banner.objects.filter(site_id=site_id).annotate(file_path=subquery_foto)[:5]
def get_announcement(site_id,lang,max_data):subquery_foto=get_photo(_B);return Announcement.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by('priority',_C)[:max_data]
def get_slideshow(site_id,lang):subquery_foto=get_photo(_L);obj=SlideShow.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:10];obj=list(obj);random.shuffle(obj);return obj
def get_fasilities(site_id,lang,exclude_id=[],is_header_text=_A,is_shuffle=_A):
	print('exclude_id',exclude_id);subquery_foto=get_photo(_T)
	if is_header_text is _A:print('isheadertext1',is_header_text);obj=Fasilities.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).annotate(file_path=subquery_foto).order_by(_D,_K)[:10];print(obj)
	else:print('isheadertext2',is_header_text);obj=Fasilities.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).exclude(is_header_text=is_header_text).annotate(file_path=subquery_foto).order_by(_D,_K)[:10]
	obj=list(obj)
	if is_shuffle:random.shuffle(obj)
	return obj
def get_offers(site_id,lang,exclude_id=[],is_header_text=_A,is_shuffle=_A):
	subquery_foto=get_photo(_U)
	if is_header_text is _A:obj=Offers.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).annotate(file_path=subquery_foto).order_by(_D,_K)[:10]
	else:obj=Offers.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).exclude(id__in=exclude_id).exclude(is_header_text=_E).annotate(file_path=subquery_foto).order_by(_D,_K)[:10]
	return obj
def get_whyus(site_id,lang):return WhyUs.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:4]
def get_dailyalert(site_id,lang):return DailyAlert.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:10]
def get_howitworks(site_id,lang):return HowItWorks.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_D,_K)[:10]
def get_aboutus(site_id,lang):subquery_foto=get_photo(_q);return AboutUs.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto)[:1]
def get_testimony(site_id,lang):subquery_foto=get_photo(_r);return Testimony.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D)[:10]
def get_product(site_id,lang):subquery_foto=get_photo(_s);return Product.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_K)[:10]
def get_greeting(site_id,lang):subquery_foto=get_photo(_H);return Greeting.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:1]
def get_events(site_id,lang):subquery_foto=get_photo(_X);return Events.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:7]
def get_photogallery(site_id,lang):subquery_foto=get_photo(_G);return PhotoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_K)[:10]
def get_videogallery(site_id,lang):subquery_foto=get_photo(_Y);return VideoGallery.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:6]
def get_relatedlink(site_id,lang):return RelatedLink.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:10]
def get_news(site_id,lang):subquery_foto=get_photo(_F);return News.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_C)[:7]
def get_article(site_id,lang):subquery_foto=get_photo(_Z);return Article.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).annotate(file_path=subquery_foto).order_by(_D,_C)[:6]
def get_document(site_id,lang):return Document.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:7]
def get_socialmedia(site_id):return SocialMedia.objects.filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_C)[:6]
def get_categories_list(site_id,lang,max_data,model):
	A='categories_id';subquery=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values(_t)[:1]);subquery_slug=Subquery(Categories.objects.translated(lang).filter(id=OuterRef(A)).values(_M)[:1]);categories_list=[];obj=model.objects.filter(site_id=site_id).values(A).annotate(count=Count(A)).annotate(name=subquery).annotate(slug=subquery_slug).order_by(A)[:max_data]
	if obj:
		all=0
		for i in obj:all+=i[_a]
		categories_list=list(obj);categories_all={A:0,_a:all,_f:'All',_M:_g};categories_list.insert(0,categories_all);return categories_list
def get_tags_list(site_id,lang,max_data,model):
	val=f"{model.__name__.lower()}__tags";subquery=Subquery(Tags.objects.translated(lang).filter(id=OuterRef(val)).values(_t)[:1]);subquery_slug=Subquery(Tags.objects.translated(lang).filter(id=OuterRef(val)).values(_M)[:1]);tags_list=[];obj=model.tags.through.objects.filter(article__site=site_id).values(val).annotate(count=Count(val)).annotate(name=subquery).annotate(slug=subquery_slug).order_by(val)[:max_data]
	if obj:
		all=0
		for i in obj:all+=i[_a]
		tags_list=list(obj);tags_all={'tags_id':0,_a:all,_f:'All',_M:_g};tags_list.insert(0,tags_all);return tags_list
def get_latest_model(site_id,lang,max_data,model,kind,slug=_A):
	subquery_foto=get_photo(kind)
	if slug:return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).exclude(slug=slug).order_by(_C)[:max_data]
	else:return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(_C)[:max_data]
def get_random_items(qs,max_data):possible_ids=list(qs.values_list('id',flat=_E));req_no_of_random_items=len(possible_ids)+1 if len(possible_ids)+1<max_data else max_data;possible_ids=random.choices(possible_ids,k=req_no_of_random_items);return qs.filter(pk__in=possible_ids)
def get_related_model(site_id,lang,max_data,model,kind,slug):
	subquery_foto=get_photo(kind);qs=model.objects.translated(lang).filter(site_id=site_id).exclude(slug=slug)
	if qs:random_paint=get_random_items(qs,max_data);random_paint=random_paint.annotate(file_path=subquery_foto);return random_paint
def get_content_detail(site_id,lang,model,kind,slug):
	print('get_content_detail',site_id,lang,model,kind,slug);subquery_foto=get_photo(kind);obj=model.objects.translated(lang).filter(site_id=site_id,slug=slug).annotate(file_path=subquery_foto)
	if obj:return obj.get()
	else:raise Http404(_b)
def get_content_list(site_id,lang,model,kind,slug):
	A='-created_at'
	if not slug:raise Http404(_b)
	subquery_foto=get_photo(kind)
	if slug==_g:return model.objects.translated(lang).filter(site_id=site_id).annotate(file_path=subquery_foto).order_by(A)
	else:
		categories=Categories.objects.filter(slug=slug);categories=categories.get()if categories else _A
		if categories:return model.objects.translated(lang).filter(site_id=site_id,categories_id=categories.id).annotate(file_path=subquery_foto).order_by(A)
		else:raise Http404('Categories '+slug+' tidak ditemukan!')
def get_location(site_id,lang):return Location.objects.language(lang).filter(site_id=site_id,status=OptStatusPublish.PUBLISHED).order_by(_D,_C)[:2]
class IndexView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		print('hostname',request.get_host());print('cokies',request.COOKIES);service=service_exists(request);print('service from index',service);service_type=service;print('servicetype',service_type)
		if not service_type:raise Http404("service belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%_N)
		self.site_id=get_site_id_front(request)
		if request.session.session_key:obj=Site.objects.get(id=self.site_id);hit_count=HitCount.objects.get_for_object(obj);HitCountMixin.hit_count(request,hit_count)
		template=get_template(self.site_id);print('template=',template);self.template_name=template+'index.html';return super(IndexView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(IndexView,self).get_context_data(*(args),**kwargs);print('execute me first');active_page=get_translated_active_page(_O);menu=get_menu_caches(self.request,_P,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);menu_footer1=get_menu_caches_footer(self.request,_h,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=_i);context.update(menu_footer1);menu_footer2=get_menu_caches_footer(self.request,_j,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=_k);context.update(menu_footer2);agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,_E);context.update(statistic);context[_J]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_p]=get_banner(self.site_id);context[_B]=get_announcement(self.site_id,lang,4);context[_L]=get_slideshow(self.site_id,lang);context['dailyalert']=get_dailyalert(self.site_id,lang);context['howitworks']=get_howitworks(self.site_id,lang);context[_q]=get_aboutus(self.site_id,lang);context[_r]=get_testimony(self.site_id,lang);context[_s]=get_product(self.site_id,lang);context['whyus']=get_whyus(self.site_id,lang);context[_T]=get_fasilities(self.site_id,lang);context[_U]=get_offers(self.site_id,lang);context[_H]=get_greeting(self.site_id,lang);context[_X]=get_events(self.site_id,lang);context[_G]=get_photogallery(self.site_id,lang);context[_Y]=get_videogallery(self.site_id,lang);context[_Q]=get_relatedlink(self.site_id,lang);context[_F]=get_news(self.site_id,lang);context[_Z]=get_article(self.site_id,lang);context[_l]=get_document(self.site_id,lang);context[_R]=get_socialmedia(self.site_id);context['location']=get_location(self.site_id,lang);context[_S]=get_base_url(self.request);return context
class DetailView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_V%(request.get_host(),_N))
		template=get_template(self.site_id);self.template_name=template+'detail.html';return super(DetailView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(DetailView,self).get_context_data(*(args),**kwargs);print('enter detail');active_page=get_translated_active_page(_O);menu=get_menu_caches(self.request,_P,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);menu_footer1=get_menu_caches_footer(self.request,_h,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=_i);context.update(menu_footer1);menu_footer2=get_menu_caches_footer(self.request,_j,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=_k);context.update(menu_footer2);context[_W]=get_menu_group(self.site_id);slug=self.kwargs[_M]
		if not slug:raise Http404(_u%(self.request.get_host(),_e))
		agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,_E);context.update(statistic);context[_J]=get_logo(self.site_id);lang=get_active_language_choices()[0];kinds=[_B,_F,_Z,_X,_l,_H,_c,_L,_T,_U];kind=self.kwargs[_d]
		if kind in kinds:context[_d]=kind
		else:raise Http404(_b)
		context[_B]=get_announcement(self.site_id,lang,6);model=apps.get_model(_I,kind)
		if kind not in[_c,_H,_L,_T,_U]:context[_m]=get_categories_list(self.site_id,lang,10,model);context[_v]=get_latest_model(self.site_id,lang,3,model,kind,slug);context[_w]=get_related_model(self.site_id,lang,5,model,kind,slug)
		else:context[_m]=get_categories_list(self.site_id,lang,10,Article);context['tags_list']=get_tags_list(self.site_id,lang,10,Article)
		content_detail=get_content_detail(self.site_id,lang,model,kind,slug);context['content_detail']=content_detail;hit_count=HitCount.objects.get_for_object(content_detail);hit_count_response=HitCountMixin.hit_count(self.request,hit_count);context[_G]=get_photogallery(self.site_id,lang);context[_Q]=get_relatedlink(self.site_id,lang);context[_T]=get_fasilities(self.site_id,lang);context[_U]=get_offers(self.site_id,lang,[content_detail.id],_E,_E);context[_R]=get_socialmedia(self.site_id);context[_S]=get_base_url(self.request);return context
class ListView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_V%(request.get_host(),_N))
		template=get_template(self.site_id);self.template_name=template+'list.html';return super(ListView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):
		context=super(ListView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_O);menu=get_menu_caches(self.request,_P,self.site_id,active_page,kinds=1,exclude_menu=0);context.update(menu);menu_footer1=get_menu_caches_footer(self.request,_h,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=_i);context.update(menu_footer1);menu_footer2=get_menu_caches_footer(self.request,_j,self.site_id,active_page,kinds=1,exclude_menu=1,parent_name=_k);context.update(menu_footer2);context[_W]=get_menu_group(self.site_id);slug=self.kwargs[_M]
		if not slug:raise Http404(_u%(self.request.get_host(),_e))
		agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,_E);context.update(statistic);context[_J]=get_logo(self.site_id);lang=get_active_language_choices()[0];kinds=[_B,_F,_Z,_X,_l,_H,_c,_L,_Y,_G];kind=self.kwargs[_d]
		if kind in kinds:context[_d]=kind
		else:raise Http404(_b)
		print('Kind = ',kind);context[_B]=get_announcement(self.site_id,lang,6);model=apps.get_model(_I,kind)
		if kind not in[_c,_H,_L,_Y,_G]:context[_m]=get_categories_list(self.site_id,lang,10,model);context[_v]=get_latest_model(self.site_id,lang,3,model,kind,slug);context[_w]=get_related_model(self.site_id,lang,5,model,kind,slug)
		print('detail model = ',model,kind);content_list=get_content_list(self.site_id,lang,model,kind,slug)
		if content_list:kind_data_per_page=8;paginator=Paginator(content_list,kind_data_per_page);page_number=self.request.GET.get('page',1);context['page_list']=paginator.get_page(page_number)
		context[_G]=get_photogallery(self.site_id,lang);context[_Q]=get_relatedlink(self.site_id,lang);context[_R]=get_socialmedia(self.site_id);context[_S]=get_base_url(self.request);return context
class DescriptionView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_V%(request.get_host(),_N))
		template=get_template(self.site_id);self.template_name=template+'description.html';return super(DescriptionView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(DescriptionView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_O);menu=get_menu_caches(self.request,_P,self.site_id,active_page,kinds=1);context.update(menu);context[_W]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,_E);context.update(statistic);context[_J]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_B]=get_announcement(self.site_id,lang,6);model=apps.get_model(_I,_B);context[_n]=get_latest_model(self.site_id,lang,3,model,_B);model=apps.get_model(_I,_F);context[_o]=get_latest_model(self.site_id,lang,3,model,_F);context[_G]=get_photogallery(self.site_id,lang);context[_Q]=get_relatedlink(self.site_id,lang);context[_R]=get_socialmedia(self.site_id);context[_S]=get_base_url(self.request);return context
class GreetingView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_V%(request.get_host(),_N))
		template=get_template(self.site_id);self.template_name=template+'greeting.html';return super(GreetingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(GreetingView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_O);menu=get_menu_caches(self.request,_P,self.site_id,active_page,1);context.update(menu);context[_W]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,_E);context.update(statistic);context[_J]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_B]=get_announcement(self.site_id,lang,6);context[_H]=get_greeting(self.site_id,lang);model=apps.get_model(_I,_B);context[_n]=get_latest_model(self.site_id,lang,3,model,_B);model=apps.get_model(_I,_F);context[_o]=get_latest_model(self.site_id,lang,3,model,_F);context[_G]=get_photogallery(self.site_id,lang);context[_Q]=get_relatedlink(self.site_id,lang);context[_R]=get_socialmedia(self.site_id);context[_S]=get_base_url(self.request);return context
class BookingView(TemplateView):
	site_id=_A
	def get(self,request,*args,**kwargs):
		self.site_id=get_site_id_front(request);service=service_exists(request)
		if not service:raise Http404(_V%(request.get_host(),_N))
		template=get_template(self.site_id);self.template_name=template+'booking.html';return super(BookingView,self).get(request,*(args),**kwargs)
	def get_context_data(self,*args,**kwargs):context=super(BookingView,self).get_context_data(*(args),**kwargs);active_page=get_translated_active_page(_O);menu=get_menu_caches(self.request,_P,self.site_id,active_page,1);context.update(menu);context[_W]=get_menu_group(self.site_id);agency=get_agency_info(self.site_id);context.update(agency);statistic=get_statistic(self.site_id,_E);context.update(statistic);context[_J]=get_logo(self.site_id);lang=get_active_language_choices()[0];context[_B]=get_announcement(self.site_id,lang,6);context[_H]=get_greeting(self.site_id,lang);model=apps.get_model(_I,_B);context[_n]=get_latest_model(self.site_id,lang,3,model,_B);model=apps.get_model(_I,_F);context[_o]=get_latest_model(self.site_id,lang,3,model,_F);context[_G]=get_photogallery(self.site_id,lang);context[_Q]=get_relatedlink(self.site_id,lang);context[_R]=get_socialmedia(self.site_id);context[_S]=get_base_url(self.request);return context