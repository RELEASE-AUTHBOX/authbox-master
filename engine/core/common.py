_A='agency'
from .models import Service,Agency,Photo,AgencyMeta
from django.db.models import OuterRef,Subquery
def get_agency_info(site_id):
	C=Service.objects.filter(site_id=site_id).values_list(_A,flat=True);D=None
	if C:E=Agency.objects.filter(id=C[0])[0];F=E.get_current_language();D=Agency.objects.language(F).filter(id=C[0])
	A={}
	if D:
		for B in D:A['uuid']=B.uuid;A['name']=B.name;A['email']=B.email;A['phone']=B.phone;A['fax']=B.fax;A['whatsapp']=B.whatsapp;A['address']=B.address;A['notes']=B.notes
	return A
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=model_name).values('file_path')[:1])
def get_agency_meta(site_id):
	D=get_photo('agencymeta');B=Service.objects.filter(site_id=site_id).values_list(_A,flat=True);A=None
	if B:
		A=Agency.objects.filter(id=B[0])
		if A:
			A=A.get();C=AgencyMeta.objects.filter(agency_id=A.id).annotate(file_path=D)[:1]
			if C:return C.get()
	return None