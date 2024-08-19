import pytz,json,os
from django.core.management.base import BaseCommand
from frontend.Google import *
from frontend.models import GoogleCalendar,GoogleCalendarDetail
from django_authbox.common import get_month_range,get_site_id_front
from datetime import datetime,timezone
from django.conf import settings
class Command(BaseCommand):
	help='Scan templates folder and save to database';template_path=settings.TEMPLATES[0]['DIRS']
	def info(self,message):self.stdout.write(message)
	def debug(self,message):self.stdout.write(message)
	def update_calendar(self):
		F='summary';E='timeZone';D='dateTime';C='end';B='start';A='description';CLIENT_SECRET_FILE='credentials/narvik/credentials.json';API_NAME='calendar';API_VERSION='v3';SCOPES=['https://www.googleapis.com/auth/calendar'];service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES);calendar_id='suratiwan03@gmail.com';timeZone='Asia/Makassar';event_request_body={B:{D:'2024-08-01T00:00:00Z',E:timeZone},C:{D:'2024-08-31T00:00:00Z',E:timeZone}};events=get_events(service,calendar_id,event_request_body)
		if events:
			gc=GoogleCalendar.objects.filter(calendar_id=calendar_id)[:1];print('gc',gc)
			if gc:
				gc=gc.get();gcd=GoogleCalendarDetail.objects.filter(google_calendar=gc);print('gcd',gcd)
				if gcd:
					print(f"Clear {len(gcd)} data")
					for i in gcd:i.delete()
				for i in events['items']:
					tmp_start=list(i[B].values())[0];year=tmp_start.split('-')[0];month=tmp_start.split('-')[1];tmp_end=list(i[C].values())[0];print('events',i['id'],i[B],i[F])
					if A in i:print(A,i[A])
					GoogleCalendarDetail.objects.create(site_id=5,google_calendar_id=gc.id,event_id=i['id'],start=tmp_start,end=tmp_end,summary=i[F],description=i[A]if A in i else None,visibility='public',location='Narvik Villa',transparency='opaque',cal_year=year,cal_month=month,cal_json=i);print('Save Complete')
			else:print('Input dulu data di Model Google Calendar')
	def handle(self,*args,**options):self.update_calendar()