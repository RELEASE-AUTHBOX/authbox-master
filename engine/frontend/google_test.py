_C='timeZone'
_B='dateTime'
_A='suratiwan03@gmail.com'
from pprint import pprint
from frontend.google import*
CLIENT_SECRET_FILE='narvik/credentials.json'
API_NAME='calendar'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/calendar']
service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
calendar_id=_A
timeZone='Asia/Makassar'
event_request_body={'start':{_B:'2024-08-01T00:00:00Z',_C:timeZone},'end':{_B:'2024-08-31T00:00:00Z',_C:timeZone},'summary':'Family Lunch','description':'Having Lunch with the parents','status':'confirmed','transparency':'opaque','visibility':'public','location':'Senggigi','attachments':[{'fileUrl':'https://drive.google.com/file/d/13VlpNIxQcrMalPWbeeZKBm_GUKg56-OM/view','title':'Meeting 2'}],'attendees':[{'displayName':'IONE','comment':'I Enjoy Coding','email':_A,'optional':False,'organizer':True,'responseStatus':'accepted'}]}
maxAttendees=5
sendNotification=True
sendUpdate=None
supportAttachments=True
get_events(service,calendar_id,event_request_body)