_A='agency'
from.models import Service,Agency,Photo,AgencyMeta
from django.db.models import OuterRef,Subquery
from django.conf import settings
def get_agency_info(site_id):
	C=Service.objects.filter(site_id=site_id).values_list(_A,flat=True);D=None
	if C:E=Agency.objects.filter(id=C[0])[0];F=E.get_current_language();D=Agency.objects.language(F).filter(id=C[0])
	A={}
	if D:
		for B in D:A['uuid']=B.uuid;A['name']=B.name;A['email']=B.email;A['phone']=B.phone;A['fax']=B.fax;A['whatsapp']=B.whatsapp;A['address']=B.address;A['notes']=B.notes;A['payment_notes']=B.payment_notes
	return A
def get_photo(model_name):return Subquery(Photo.objects.filter(object_id=OuterRef('id'),content_type__model=model_name).values('file_path')[:1])
def get_agency_meta(request,site_id):
	G='http';F='https';B=request;H=get_photo('agencymeta');E=Service.objects.filter(site_id=site_id).values_list(_A,flat=True);C=None
	if E:
		C=Agency.objects.filter(id=E[0])
		if C:
			C=C.get();A=AgencyMeta.objects.filter(agency_id=C.id).annotate(file_path=H)[:1]
			if A:
				A=A.get();D=settings.MEDIA_URL
				if A.file_path:
					if not A.file_path.startswith(('http://','https://')):
						if B:
							if not A.file_path.startswith(D):A.file_path='%s://%s%s%s'%(F if B.is_secure()else G,B.get_host(),D,A.file_path)
							else:A.file_path='%s://%s%s'%(F if B.is_secure()else G,B.get_host(),A.file_path)
						elif not A.file_path.startswith(D):A.file_path=f"{D}{A.file_path}"
				return A