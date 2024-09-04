_C='summary'
_B='start'
_A='dateTime'
from pprint import pprint
import pickle,os,datetime
from collections import namedtuple
from google_auth_oauthlib.flow import Flow,InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload
from google.auth.transport.requests import Request
from os.path import dirname
import pytz
def create_service(client_secret_file,api_name,api_version,*J,prefix=''):
	H=client_secret_file;D=api_name;K=H;F=api_version;L=[A for A in J[0]];A=None;B=os.getcwd();C='token files';E=f"token_{D}_{F}{prefix}.pickle";I=dirname(os.path.join(B,H))
	if I:C=I
	if not os.path.exists(os.path.join(B,C)):os.mkdir(os.path.join(B,C))
	if os.path.exists(os.path.join(B,C,E)):
		with open(os.path.join(B,C,E),'rb')as G:A=pickle.load(G)
	if not A or not A.valid:
		if A and A.expired and A.refresh_token:A.refresh(Request())
		else:M=InstalledAppFlow.from_client_secrets_file(K,L);A=M.run_local_server()
		with open(os.path.join(B,C,E),'wb')as G:pickle.dump(A,G)
	try:N=build(D,F,credentials=A);return N
	except Exception as O:os.remove(os.path.join(B,C,E));return
def convert_to_RFC_datetime(year=1900,month=1,day=1,hour=0,minute=0):A=datetime.datetime(year,month,day,hour,minute,0).isoformat()+'Z';return A
def create_events(service,calendar_id,event_request_body,sendNotification,sendUpdate):A=service.events().insert(calendarId=calendar_id,sendNotifications=sendNotification,sendUpdates=sendUpdate,body=event_request_body).execute();return A
def already_exists(service,calendar_id,new_event):
	A=new_event;B=get_date_events(A[_B][_A],get_events(service,calendar_id));C=[A[_C]for A in B];
	if A[_C]not in C:return False
	return True
def get_date_events(date,events):
	A=date;C=[];A=A
	for B in events:
		if B.get(_B).get(_A):
			D=B[_B][_A]
			if D==A:C.append(B)
	return C
def get_events(service,calendar_id,new_event):B='end';A=new_event;D=A[_B].get(_A);E=A[B].get(_A);C=service.events().list(calendarId=calendar_id,timeMin=A[_B][_A],timeMax=A[B][_A]).execute();return C
def list_calendars(service):
	C=service.calendarList().list().execute();A=C.get('items',[]);
	if not A:pass
	for B in A:D=B[_C];id=B['id'];