_H='/admin'
_G="template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_F='CPANEL_DOMAIN'
_E='CPANEL_URL'
_D='CPANEL_TOKEN'
_C='CPANEL_USER'
_B=False
_A=True
import pytz,calendar,os
from datetime import datetime,timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from core.models import Service,Template,User
def get_site_id(request):
	E='-is_default';D=request
	if not D:return-1
	F=D.user.id
	if not F:return-1
	C=User.objects.filter(id=D.user.id)
	if not C:return-2
	C=C.get();A=C.agency.all().order_by(E)
	if not A:return-3
	if len(A)>1:return-31
	A=A[0];print('agency == ',A);B=Service.objects.filter(agency_id=A.id).order_by(E)
	if not B:return-4
	if len(B)>1:return-41
	B=B[0]
	if B:return B.site_id
	return 0
def get_site_id_front(request):
	A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=_A)
	if A:return A[0]
	return 0
def get_agency_from(request):A=User.objects.get(id=request.user.id);B=A.agency.all()[0];return B.id
def create_sub_domain(sub_domain):
	A=getattr(settings,_C,'');D=getattr(settings,_D,'');E=getattr(settings,_E,'');F=getattr(settings,_F,'');print('cpanel_user',A);B=-1
	if A:
		G='/public_html';H=f"curl -H'Authorization: cpanel {A}:{D}' 'https://{E}:2083/json-api/cpanel?cpanel_jsonapi_func=addsubdomain&cpanel_jsonapi_module=SubDomain&cpanel_jsonapi_version=2&domain={sub_domain}&rootdomain={F}&dir={G}'";C=3
		while B!=0:
			B=os.system(H);C-=1
			if C<=0:break
	if B==0:return _A
	return _B
def delete_sub_domain(sub_domain):
	A=getattr(settings,_C,'');B=getattr(settings,_D,'');C=getattr(settings,_E,'');D=getattr(settings,_F,'')
	if A:E=f"curl -H'Authorization: cpanel {A}:{B}' 'https://{C}:2083/json-api/cpanel?cpanel_jsonapi_func=delsubdomain&cpanel_jsonapi_module=SubDomain&cpanel_jsonapi_version=2&domain={sub_domain}.{D}'";F=os.popen(E);return _A
	return _B
def get_template_id(site_id,is_frontend=_A):
	A=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list('id',flat=_A)[:1]
	if A:return A[0]
	raise Http404(_G%_H)
def get_template(site_id,is_frontend=_A):
	A=Template.objects.filter(site__id=site_id,is_frontend=is_frontend).values_list('rel_path',flat=_A)[:1]
	if A:return A[0]
	raise Http404(_G%_H)
def get_week_date(year,month,day):
	A=calendar.Calendar();A=A.monthdatescalendar(year,month);E=_B;D=0
	for D in range(0,len(A)-1):
		for F in A[D]:
			if F.day==day:E=_A;break
		if E:break
	B=A[D][0];B=datetime(B.year,B.month,B.day,0,0,0);C=A[D][6];C=datetime(C.year,C.month,C.day,23,59,59);return B,C
def get_month_range(date):A=date;B=calendar.monthrange(A.year,A.month)[1];C=datetime(A.year,A.month,1);D=datetime(A.year,A.month,B,23,59,59);return C,D
def add_months(sourcedate,months):B=sourcedate;A=B.month-1+months;C=B.year+A//12;A=A%12+1;D=min(B.day,calendar.monthrange(C,A)[1]);return datetime(C,A,D)
def get_natural_datetime(data_datetime):
	B=data_datetime
	if not B:return B
	E=getattr(settings,'TIME_ZONE','UTC');M=pytz.timezone(E);A=timezone.now();F=A-timedelta(hours=24);G=A-timedelta(hours=48);H=A-timedelta(days=7);I=A-timedelta(days=14);J=A-timedelta(days=21);K=A-timedelta(days=28);D=calendar.monthrange(A.year,A.month)[1];L=A-timedelta(days=D+1)
	if F<B<A:return naturaltime(B)
	elif G<B<A:return naturalday(B)
	elif H<B<A:return _(B.strftime('%A'))
	elif I<B<A:
		C=(A-B).days-7
		if C==0:return _('Seminggu yang lalu')
	elif J<B<A:
		C=(A-B).days-14
		if C==0:return _('Dua minggu yang lalu')
	elif K<B<A:
		C=(A-B).days-21
		if C==0:return _('Tiga minggu yang lalu')
	elif L<B<A:
		C=(A-B).days-D
		if C==0:return _('Sebulan yang lalu')
	return naturalday(B)
def get_format_date():A=datetime.now();return A.strftime('%A, %d %B %Y')