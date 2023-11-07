_A='agency'
from .models import Service,Agency,Photo,AgencyMeta
from django.db.models import OuterRef,Subquery
from django.conf import settings
def get_agency_info(site_id):
	C=Service.objects.filter(site_id=site_id).values_list(_A,flat=True);D=None
	if C:E=Agency.objects.filter(id=C[0])[0];F=E.get_current_language();D=Agency.objects.language(F).filter(id=C[0])
	A={}
	if D:
		for B in D:A['uuid']=B.uuid;A['name']=B.name;A['email']=B.email;A['phone']=B.phone;A['fax']=B.fax;A['whatsapp']=B.whatsapp;A['address']=B.address;A['notes']=B.notes
	return A
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=model_name).values('file_path')[:1])
def get_agency_meta(request,site_id):
	C=request;E=get_photo('agencymeta');D=Service.objects.filter(site_id=site_id).values_list(_A,flat=True);B=None
	if D:
		B=Agency.objects.filter(id=D[0])
		if B:
			B=B.get();A=AgencyMeta.objects.filter(agency_id=B.id).annotate(file_path=E)[:1]
			if A:A=A.get();F=settings.MEDIA_URL;A.file_path='%s://%s%s%s'%('https'if C.is_secure()else'http',C.get_host(),F,A.file_path);return A
	return None