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
	J='summary';I='timeZone';H='dateTime';G='end';F='T00:00:00Z';E='start';D='items';C='description';B='-';A='id';site=Site.objects.filter(domain=domain)[:1];print('SITE = ',site)
	if not site:sys.stdout.write('Site Not Found!\n');return _A
	site=site.get();site_id=site.id;print('site_id',site_id);cal=GoogleCalendar.objects.filter(site=site)[:1]
	if not cal:sys.stdout.write('Calendar Not Found!\n');return _A
	cal=cal.get();CLIENT_SECRET_FILE=cal.file_path_doc.path;calendar_id=cal.calendar_id;print('calendar_id',calendar_id);API_NAME='calendar';API_VERSION='v3';SCOPES=['https://www.googleapis.com/auth/calendar'];service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES);result=service.calendarList().list().execute();mfound=False
	for i in result[D]:
		print('calendar List',i[A])
		if i[A]==calendar_id:mfound=True;break
	if not mfound:sys.stdout.write(calendar_id+' Not found in Calendar List!\n');return _A
	year=datetime.now().year;num_days=monthrange(year,int(month_end))[1];timeZone='Asia/Makassar';event_request_body={E:{H:str(year)+B+str(month_start)+'-01T00:00:00Z',I:timeZone},G:{H:str(year)+B+str(month_end)+B+str(num_days)+F,I:timeZone}};print('event_request_body',event_request_body);gcd=GoogleCalendarDetail.objects.filter(google_calendar=cal);print('gcd',gcd)
	if gcd:
		print(f"Clear {len(gcd)} data")
		for i in gcd:i.delete()
	for j in result[D]:
		calendar_id=j[A];events=get_events(service,calendar_id,event_request_body)
		if events:
			for i in events[D]:
				print('Proses ',i);tmp_start=list(i[E].values())[0];year=tmp_start.split(B)[0];month=tmp_start.split(B)[1];tmp_end=list(i[G].values())[0];print('events',i[A],i[E],i[J])
				if C in i:print(C,i[C])
				GoogleCalendarDetail.objects.create(site_id=site_id,google_calendar_id=cal.id,event_id=i[A],start=tmp_start+F,end=tmp_end+F,summary=i[J],description=i[C]if C in i else _A,visibility='public',location='Narvik Villa',transparency='opaque',cal_year=year,cal_month=month,cal_json=i);print('Save Complete')