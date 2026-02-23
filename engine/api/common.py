from django.contrib.sites.models import Site
def get_site_id(request):
	A=Site.objects.filter(domain=request.get_host()).values_list('id',flat=True)
	if A:return A[0]
	return 0