_D='month_end'
_C='month_start'
_B='domain'
_A=None
from django.contrib.sites.models import Site
import pytz,json,os,sys
from django.core.management.base import BaseCommand
from frontend.Google import *
from frontend.models import GoogleCalendar,GoogleCalendarDetail
from django_authbox.common import get_month_range,get_site_id_front
from datetime import datetime,timezone
from django.conf import settings
from calendar import monthrange
exposed_request=_A
class Command(BaseCommand):
	help='Scan templates folder and save to database';template_path=settings.TEMPLATES[0]['DIRS']
	def info(self,message):sys.stdout.write(message)
	def debug(self,message):sys.stdout.write(message)
	def add_arguments(self,parser):parser.add_argument(_B,type=str);parser.add_argument(_C,type=str);parser.add_argument(_D,type=str)
	def handle(self,*args,**options):domain=options[_B];month_start=options[_C];month_end=options[_D];update_calendar(domain,month_start,month_end)
def update_calendar(domain,month_start,month_end):
	H='summary';G='timeZone';F='dateTime';E='end';D='T00:00:00Z';C='start';B='description';A='-';site=Site.objects.filter(domain=domain)[:1];print('SITE = ',site)
	if not site:sys.stdout.write('Site Not Found!\n');return _A
	site=site.get();cal=GoogleCalendar.objects.filter(site=site)[:1]
	if not cal:sys.stdout.write('Calendar Not Found!\n');return _A
	cal=cal.get();CLIENT_SECRET_FILE=cal.file_path_doc.path;calendar_id=cal.calendar_id;print('calendar_id',calendar_id);API_NAME='calendar';API_VERSION='v3';SCOPES=['https://www.googleapis.com/auth/calendar'];service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES);year=datetime.now().year;num_days=monthrange(year,int(month_end))[1];timeZone='Asia/Makassar';event_request_body={C:{F:str(year)+A+str(month_start)+'-01T00:00:00Z',G:timeZone},E:{F:str(year)+A+str(month_end)+A+str(num_days)+D,G:timeZone}};print('event_request_body',event_request_body);events=get_events(service,calendar_id,event_request_body)
	if events:
		gcd=GoogleCalendarDetail.objects.filter(google_calendar=cal);print('gcd',gcd)
		if gcd:
			print(f"Clear {len(gcd)} data")
			for i in gcd:i.delete()
		for i in events['items']:
			print('Proses ',i);tmp_start=list(i[C].values())[0];year=tmp_start.split(A)[0];month=tmp_start.split(A)[1];tmp_end=list(i[E].values())[0];print('events',i['id'],i[C],i[H])
			if B in i:print(B,i[B])
			GoogleCalendarDetail.objects.create(site_id=5,google_calendar_id=cal.id,event_id=i['id'],start=tmp_start+D,end=tmp_end+D,summary=i[H],description=i[B]if B in i else _A,visibility='public',location='Narvik Villa',transparency='opaque',cal_year=year,cal_month=month,cal_json=i);print('Save Complete')