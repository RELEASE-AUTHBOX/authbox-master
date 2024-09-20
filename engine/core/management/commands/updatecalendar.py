_C='month_end'
_B='month_start'
_A='domain'
from django.contrib.sites.models import Site
import pytz,json,os,sys
from django.core.management.base import BaseCommand
from frontend.Google import*
from frontend.models import GoogleCalendar,GoogleCalendarDetail
from django_authbox.common import get_month_range,get_site_id_front
from datetime import datetime,timezone
from django.conf import settings
from calendar import monthrange
exposed_request=None
class Command(BaseCommand):
	help='Scan templates folder and save to database';template_path=settings.TEMPLATES[0]['DIRS']
	def info(self,message):sys.stdout.write(message)
	def debug(self,message):sys.stdout.write(message)
	def add_arguments(self,parser):parser.add_argument(_A,type=str);parser.add_argument(_B,type=str);parser.add_argument(_C,type=str)
	def handle(self,*args,**options):domain=options[_A];month_start=options[_B];month_end=options[_C];update_calendar(domain,month_start,month_end)
def update_calendar(domain,month_start,month_end):
	G='summary';F='timeZone';E='dateTime';D='end';C='start';B='description';A='-';site=Site.objects.filter(domain=domain)[:1];
	if not site:sys.stdout.write('Site Not Found!\n');return
	site=site.get();cal=GoogleCalendar.objects.filter(site=site)[:1]
	if not cal:sys.stdout.write('Calendar Not Found!\n');return
	cal=cal.get();CLIENT_SECRET_FILE=cal.file_path_doc.path;calendar_id=cal.calendar_id;API_NAME='calendar';API_VERSION='v3';SCOPES=['https://www.googleapis.com/auth/calendar'];service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES);year=datetime.now().year;num_days=monthrange(year,int(month_end))[1];timeZone='Asia/Makassar';event_request_body={C:{E:str(year)+A+str(month_start)+'-01T00:00:00Z',F:timeZone},D:{E:str(year)+A+str(month_end)+A+str(num_days)+'T00:00:00Z',F:timeZone}};events=get_events(service,calendar_id,event_request_body)
	if events:
		gcd=GoogleCalendarDetail.objects.filter(google_calendar=cal);
		if gcd:
			for i in gcd:i.delete()
		for i in events['items']:
			tmp_start=list(i[C].values())[0];year=tmp_start.split(A)[0];month=tmp_start.split(A)[1];tmp_end=list(i[D].values())[0];
			if B in i:pass
			GoogleCalendarDetail.objects.create(site_id=5,google_calendar_id=cal.id,event_id=i['id'],start=tmp_start,end=tmp_end,summary=i[G],description=i[B]if B in i else None,visibility='public',location='Narvik Villa',transparency='opaque',cal_year=year,cal_month=month,cal_json=i);