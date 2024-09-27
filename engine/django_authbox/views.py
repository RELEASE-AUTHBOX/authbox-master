from django.http import Http404
from django.shortcuts import redirect
from core.models import Service
from.common import get_site_id_front
def service_exists(request):
	B=get_site_id_front(request);A=Service.objects.filter(site_id=B)
	if A:return A.get().get_kind_display().lower()
def redirect_service(request):
	A=request
	if service_exists(A):return redirect('/id/')
	raise Http404("service untuk '%s' belum terdaftar, silahkan daftar di halaman <a href='%s'>admin</a>"%(A.get_host(),'/admin'))