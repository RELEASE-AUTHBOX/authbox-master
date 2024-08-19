_I='/admin'
_H="template belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"
_G='template'
_F='CPANEL_DOMAIN'
_E='CPANEL_URL'
_D='CPANEL_TOKEN'
_C='CPANEL_USER'
_B=False
_A=True
import pytz,calendar,os
from datetime import datetime,timedelta
from core.models import Service,Template,User
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturalday,naturaltime
from django.contrib.sites.models import Site
from django.http import Http404
from django.utils.translation import gettext_lazy as _
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
def get_site_id_front(request):
	A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=_A)
	if A:return A[0]
	return 0
def get_template_id(site_id,is_frontend=_A):
	B=site_id;print('site',B);A=Template.objects.filter(site__id=B,is_frontend=is_frontend).values_list('id',flat=_A)[:1];print(_G,A)
	if A:return A[0]
	raise Http404(_H%_I)
def get_template(site_id,is_frontend=_A):
	B=site_id;print('site',B);A=Template.objects.filter(site__id=B,is_frontend=is_frontend).values_list('rel_path',flat=_A)[:1];print(_G,A)
	if A:return A[0]
	raise Http404(_H%_I)
def get_week_date(year,month,day):
	A=calendar.Calendar();A=A.monthdatescalendar(year,month);E=_B;D=0
	for D in range(0,len(A)-1):
		for F in A[D]:
			if F.day==day:E=_A;break
		if E:break
	B=A[D][0];B=datetime(B.year,B.month,B.day,0,0,0);C=A[D][6];C=datetime(C.year,C.month,C.day,23,59,59);return B,C
def get_month_range(date):A=date;B=calendar.monthrange(A.year,A.month)[1];C=datetime(A.year,A.month,1);D=datetime(A.year,A.month,B,23,59,59);return C,D
def add_months(sourcedate,months):B=sourcedate;A=B.month-1+months;C=B.year+A//12;A=A%12+1;D=min(B.day,calendar.monthrange(C,A)[1]);return datetime(C,A,D)
def get_natural_datetime(data_datetime,skrg=datetime.now()):
	I='a week ago';C=data_datetime;A=skrg;J=datetime(A.year,A.month,A.day,0,0,0);K=datetime(A.year,A.month,A.day,23,59,59);E=A-timedelta(days=1);L=datetime(E.year,E.month,E.day,0,0,0);M=datetime(E.year,E.month,E.day,23,59,59);G,H=get_week_date(A.year,A.month,A.day);N=G-timedelta(days=7);O=H-timedelta(days=7);P=G-timedelta(days=14);Q=H-timedelta(days=14);R=G-timedelta(days=21);S=H-timedelta(days=21);F=calendar.monthrange(A.year,A.month)[1];T=datetime(A.year,A.month,1,0,0,0);U=datetime(A.year,A.month,F,23,59,59);D=add_months(A,-1);F=calendar.monthrange(D.year,D.month)[1];V=datetime(D.year,D.month,1,0,0,0);W=datetime(D.year,D.month,F,23,59,59);D=add_months(A,-2);F=calendar.monthrange(D.year,D.month)[1];X=datetime(D.year,D.month,1,0,0,0);Y=datetime(D.year,D.month,F,23,59,59);B=pytz.UTC
	if B.localize(J)<=C<=B.localize(K):return naturaltime(C)
	elif B.localize(L)<=C<=B.localize(M):return naturalday(C)
	elif B.localize(G)<=C<=B.localize(H):return _(C.strftime('%A'))
	elif B.localize(N)<=C<=B.localize(O):
		if C.weekday()==6:return _(I)
		else:return _(I)+', '+_(C.strftime('%A'))
	elif B.localize(P)<=C<=B.localize(Q)and B.localize(A.weekday())==C.weekday():return _('two weeks ago')
	elif B.localize(R)<=C<=B.localize(S)and B.localize(A.weekday())==C.weekday():return _('three weeks ago')
	elif B.localize(T)<=C<=B.localize(U):return _('this month')
	elif B.localize(V)<=C<=B.localize(W)and (A-C).days>=30:return _('a month ago')
	elif B.localize(X)<=C<=B.localize(Y)and (A-C).days>=60:return _('two months ago')
	return naturalday(C)