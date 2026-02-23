_b='setting_name'
_a='domain'
_Z='code field is required'
_Y='Invalid parent ID'
_X='Invalid code'
_W='value_text'
_V='template'
_U='delete'
_T='-created_at'
_S='setting_value'
_R='value_type'
_Q='is_active'
_P='message'
_O='created_at'
_N='Content not found'
_M='name'
_L='content_type'
_K='Authentication required'
_J='object_id'
_I='site'
_H=True
_G='get'
_F='code'
_E=None
_D='request'
_C=False
_B='parent'
_A='error'
from rest_framework import viewsets,filters,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.sites.models import Site
from django_filters.rest_framework import DjangoFilterBackend
from.models import Photo,Content,SiteMetadata,Template,UserSettings,UserProfile
from.serializers import PhotoSerializer,ContentSerializer,ContentListSerializer,ContentCreateUpdateSerializer,SiteSerializer,SiteMetadataSerializer,TemplateSerializer,UserSettingsSerializer,UserProfileSerializer
from.common import get_site_id
from.encryption import decrypt_data
class CustomPageNumberPagination(PageNumberPagination):page_size=10;page_size_query_param='page_size';max_page_size=10000
class PhotoViewSet(viewsets.ModelViewSet):
	queryset=Photo.objects.all();serializer_class=PhotoSerializer;filter_backends=[DjangoFilterBackend,filters.OrderingFilter];filterset_fields=[_L,_J];ordering_fields=[_O,'title'];ordering=[_T]
	def list(A,request,*D,**E):B=A.get_queryset();print('PhotoViewSet list - original queryset count:',B.count());C=A.get_serializer(B,many=_H);return Response(C.data)
	def get_queryset(C):
		A=super().get_queryset();B=C.request.query_params.get(_J)
		if B:print(f"PhotoViewSet get_queryset - filtering by object_id: {B}");A=A.filter(object_id=B);print(f"PhotoViewSet get_queryset - filtered queryset count: {A.count()}")
		return A
	def perform_create(D,serializer):
		B=serializer;A=D.request.data.get(_J)
		if A:C=decrypt_data(str(A));print(f"PhotoViewSet create - encrypted object_id: {A}");print(f"PhotoViewSet create - decrypted object_id: {C}");B.save(object_id=int(C))
		else:B.save()
	def perform_update(D,serializer):
		B=serializer;A=D.request.data.get(_J)
		if A:C=decrypt_data(str(A));print(f"PhotoViewSet update - encrypted object_id: {A}");print(f"PhotoViewSet update - decrypted object_id: {C}");B.save(object_id=int(C))
		else:B.save()
	def perform_delete(C,serializer):
		A=C.request.data.get(_J);print('PhotoViewSet delete - object_id:',A)
		if A:B=decrypt_data(str(A));print(f"PhotoViewSet delete - encrypted object_id: {A}");print(f"PhotoViewSet delete - decrypted object_id: {B}");serializer.delete(object_id=int(B))
	@action(detail=_C,methods=[_U],url_path='delete-by-object-id')
	def delete_by_object_id(self,request):
		B=request;A=B.data.get(_J)or B.query_params.get(_J)
		if not A:return Response({_A:'object_id parameter is required'},status=status.HTTP_400_BAD_REQUEST)
		C=decrypt_data(str(A));print(f"PhotoViewSet delete_by_object_id - encrypted object_id: {A}");print(f"PhotoViewSet delete_by_object_id - decrypted object_id: {C}");D=Photo.objects.filter(object_id=int(C));E=D.count();D.delete();return Response({_P:f"Deleted {E} photo(s)",'count':E},status=status.HTTP_200_OK)
	@action(detail=_C,methods=[_G],url_path='content-type-id')
	def get_content_type_id(self,request):from django.contrib.contenttypes.models import ContentType as A;B=A.objects.get_for_model(Content);return Response({'content_type_id':B.id})
class TemplateViewSet(viewsets.ModelViewSet):queryset=Template.objects.all();serializer_class=TemplateSerializer;filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter];filterset_fields=[_Q];search_fields=[_M,'description'];ordering_fields=[_M,_O];ordering=[_M]
class ContentViewSet(viewsets.ModelViewSet):
	queryset=Content.objects.select_related(_I,_B,_V).prefetch_related('value_image','children');pagination_class=CustomPageNumberPagination;filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter];filterset_fields=[_I,_F,_R,_L,_B,_Q,_V];search_fields=[_F,_W,'value_textarea'];ordering_fields=['order',_O,_F];ordering=[_T,'order']
	def get_serializer_class(A):
		if A.action=='list':return ContentListSerializer
		elif A.action in['create','update','partial_update']:return ContentCreateUpdateSerializer
		return ContentSerializer
	def get_queryset(B):
		A=super().get_queryset();C=get_site_id(B.request)
		if C:A=A.filter(site_id=C)
		D=B.request.query_params.get('root_only',_E)
		if D and D.lower()=='true':A=A.filter(parent__isnull=_H)
		return A
	@action(detail=_C,methods=[_G])
	def navigation(self,request):A=request;B=get_site_id(A);C=self.get_queryset().filter(site_id=B,content_type=4,parent__isnull=_H);D=ContentSerializer(C,many=_H,context={_D:A});return Response(D.data)
	@action(detail=_C,methods=[_G],url_path='navigation/top')
	def navigation_top(self,request):
		A=request;B=get_site_id(A)
		try:C=Content.objects.get(site_id=B,content_type=4,code='top_menu');D=self.get_queryset().filter(site_id=B,content_type=4,parent=C);E=ContentSerializer(D,many=_H,context={_D:A});return Response(E.data)
		except Content.DoesNotExist:return Response([])
	@action(detail=_C,methods=[_G],url_path='navigation/bottom')
	def navigation_bottom(self,request):
		A=request;B=get_site_id(A)
		try:C=Content.objects.get(site_id=B,content_type=4,code='bottom_menu');D=self.get_queryset().filter(site_id=B,content_type=4,parent=C);E=ContentSerializer(D,many=_H,context={_D:A});return Response(E.data)
		except Content.DoesNotExist:return Response([])
	@action(detail=_C,methods=[_G])
	def by_code(self,request):
		A=request;B=A.query_params.get(_F,_E);E=get_site_id(A)
		if not B:return Response({_A:'code parameter is required'},status=status.HTTP_400_BAD_REQUEST)
		try:C=decrypt_data(B);print(f"by_code - encrypted code: {B}");print(f"by_code - decrypted code: {C}")
		except Exception as F:print(f"Error decrypting code: {F}");return Response({_A:_X},status=status.HTTP_400_BAD_REQUEST)
		G=self.get_queryset().filter(code=C,site_id=E);D=G.first()
		if not D:return Response({_A:_N},status=status.HTTP_404_NOT_FOUND)
		H=ContentSerializer(D,context={_D:A});return Response(H.data)
	@action(detail=_C,methods=[_G])
	def by_slug(self,request):
		A=request;B=A.query_params.get('slug',_E);D=get_site_id(A)
		if not B:return Response({_A:'slug parameter is required'},status=status.HTTP_400_BAD_REQUEST)
		E=self.get_queryset().filter(slug=B,site_id=D);C=E.first()
		if not C:return Response({_A:_N},status=status.HTTP_404_NOT_FOUND)
		F=ContentSerializer(C,context={_D:A});return Response(F.data)
	@action(detail=_C,methods=['POST'])
	def create_navigation(self,request):
		B=request;print('DEBUG: create_navigation called');D=get_site_id(B);print(f"DEBUG: site_id={D}");A=B.data.copy();E=A.pop('location',_E)
		if E and not A.get(_B):
			F=f"{E}_menu";H,I=Content.objects.get_or_create(site_id=D,code=F,defaults={_L:4,_R:1,_W:f"{E.title()} Menu",'slug':F,_Q:_H})
			if I:print(f"DEBUG: Created location container: {F}")
			A[_B]=H.id
		if not A.get(_F):import time;A[_F]=f"menu_{int(time.time()*1000)}"
		A[_I]=D;A[_L]=4;A[_R]=1
		if A.get(_B)and isinstance(A[_B],str):
			try:A[_B]=decrypt_data(A[_B]);print(f"DEBUG: Decrypted parent={A[_B]}")
			except Exception as J:print('Error decrypting parent:',J);return Response({_A:_Y},status=status.HTTP_400_BAD_REQUEST)
		print(f"DEBUG: Data to serialize: {A}");C=ContentCreateUpdateSerializer(data=A,context={_D:B})
		if C.is_valid():G=C.save();print(f"DEBUG: Saved content: {G.id}, code={G.code}");K=ContentSerializer(G,context={_D:B});return Response(K.data,status=status.HTTP_201_CREATED)
		print('DEBUG: Serializer errors:',C.errors);return Response(C.errors,status=status.HTTP_400_BAD_REQUEST)
	@action(detail=_C,methods=['POST'])
	def custom_post(self,request):
		C=request;I=get_site_id(C);A=C.data.copy();E=A.get(_F,_E)
		if E:
			try:F=decrypt_data(E);print(f"custom_post - encrypted code: {E}");print(f"custom_post - decrypted code: {F}")
			except Exception as D:print(f"Error decrypting code: {D}");return Response({_A:_X},status=status.HTTP_400_BAD_REQUEST)
			J=Content.objects.filter(code=F,site_id=I).first()
			if J:
				A.pop(_F,_E);A.pop(_I,_E)
				if A.get(_B):
					try:A[_B]=decrypt_data(A[_B])
					except Exception as D:print(f"Error decrypting parent: {D}");pass
				B=ContentCreateUpdateSerializer(J,data=A,partial=_H,context={_D:C})
				if B.is_valid():G=B.save();H=ContentSerializer(G,context={_D:C});return Response(H.data,status=status.HTTP_200_OK)
				return Response(B.errors,status=status.HTTP_400_BAD_REQUEST)
		A[_I]=I
		if not A.get(_F):import time;A[_F]=f"content_{int(time.time()*1000)}"
		else:A[_F]=F
		if A.get(_B):
			try:A[_B]=decrypt_data(A[_B])
			except Exception as D:print(f"Error decrypting parent: {D}");return Response({_A:_Y},status=status.HTTP_400_BAD_REQUEST)
		B=ContentCreateUpdateSerializer(data=A,context={_D:C})
		if B.is_valid():G=B.save();H=ContentSerializer(G,context={_D:C});return Response(H.data,status=status.HTTP_201_CREATED)
		return Response(B.errors,status=status.HTTP_400_BAD_REQUEST)
	@action(detail=_C,methods=['put','patch'])
	def update_by_code(self,request):
		C=request;print('DEBUG: update_by_code called');B=C.data.get(_F,_E);F=get_site_id(C);print(f"DEBUG: site_id={F}, code (encrypted)={B}");B=decrypt_data(B);print(f"DEBUG: Decrypted code={B}")
		if not B:return Response({_A:_Z},status=status.HTTP_400_BAD_REQUEST)
		G=self.get_queryset().filter(code=B,site_id=F);E=G.first()
		if not E:print('DEBUG: Content not found');return Response({_A:_N},status=status.HTTP_404_NOT_FOUND)
		print(f"DEBUG: Found content {E.id}");H=self.get_serializer_class();I=C.method=='PATCH';A=C.data.copy();A.pop(_F,_E);A.pop(_I,_E)
		if A.get(_B):
			try:A[_B]=decrypt_data(A[_B]);print(f"DEBUG: Decrypted parent={A[_B]}")
			except Exception as J:print(f"DEBUG: Parent decryption failed: {J}");pass
		print(f"DEBUG: Data for update: {A}");D=H(E,data=A,partial=I,context={_D:C})
		if D.is_valid():K=D.save();print(f"DEBUG: Updated content {K.id}");return Response(D.data)
		print('DEBUG: Update serializer errors:',D.errors);return Response(D.errors,status=status.HTTP_400_BAD_REQUEST)
	@action(detail=_C,methods=[_U])
	def delete_by_code(self,request):
		C=request;A=C.data.get(_F,_E);E=get_site_id(C)
		if not A:return Response({_A:_Z},status=status.HTTP_400_BAD_REQUEST)
		D=decrypt_data(A);print('Encrypted code:',A);print('Decrypted code:',D);F=self.get_queryset().filter(code=D,site_id=E);B=F.first()
		if not B:return Response({_A:_N},status=status.HTTP_404_NOT_FOUND)
		G=B.code;B.delete();return Response({_P:f'Content "{G}" deleted successfully'},status=status.HTTP_200_OK)
class SiteViewSet(viewsets.ReadOnlyModelViewSet):queryset=Site.objects.all();serializer_class=SiteSerializer;filter_backends=[filters.SearchFilter];search_fields=[_a,_M]
class SiteMetadataViewSet(viewsets.ModelViewSet):
	queryset=SiteMetadata.objects.select_related(_I);serializer_class=SiteMetadataSerializer;filter_backends=[DjangoFilterBackend,filters.SearchFilter];filterset_fields=[_I];search_fields=['site_title','site_tagline','meta_description']
	@action(detail=_C,methods=[_G])
	def by_site(self,request):
		A=request;B=A.query_params.get('site_id',_E);C=A.query_params.get(_a,_E)
		if not B and not C:return Response({_A:'Either site_id or domain parameter is required'},status=status.HTTP_400_BAD_REQUEST)
		try:
			if B:D=SiteMetadata.objects.get(site_id=B)
			else:E=Site.objects.get(domain=C);D=SiteMetadata.objects.get(site=E)
			F=self.get_serializer(D,context={_D:A});return Response(F.data)
		except(SiteMetadata.DoesNotExist,Site.DoesNotExist):return Response({_A:'Metadata not found'},status=status.HTTP_404_NOT_FOUND)
class UserSettingsViewSet(viewsets.ViewSet):
	@action(detail=_C,methods=[_G])
	def all(self,request):
		A=request
		if not A.user.is_authenticated:return Response({_A:_K},status=status.HTTP_401_UNAUTHORIZED)
		B=UserSettingsSerializer(A.user,context={_D:A});return Response(B.data)
	@action(detail=_C,methods=['post'])
	def bulk_update(self,request):
		A=request
		if not A.user.is_authenticated:return Response({_A:_K},status=status.HTTP_401_UNAUTHORIZED)
		B=UserSettingsSerializer(data=A.data,context={_D:A})
		if B.is_valid():B.update(A.user,B.validated_data);C=UserSettingsSerializer(A.user,context={_D:A});return Response(C.data,status=status.HTTP_200_OK)
		return Response(B.errors,status=status.HTTP_400_BAD_REQUEST)
	@action(detail=_C,methods=[_G],url_path='get/(?P<setting_name>[^/.]+)')
	def get_setting(self,request,setting_name=_E):
		B=setting_name;A=request
		if not A.user.is_authenticated:return Response({_A:_K},status=status.HTTP_401_UNAUTHORIZED)
		C=get_site_id(A);D=Site.objects.get(id=C);E=UserSettings.get_default_settings();F=UserSettings.get_setting(A.user,D,B,default=E.get(B,''));return Response({_b:B,_S:F})
	@action(detail=_C,methods=['post'],url_path='set/(?P<setting_name>[^/.]+)')
	def set_setting(self,request,setting_name=_E):
		B=setting_name;A=request
		if not A.user.is_authenticated:return Response({_A:_K},status=status.HTTP_401_UNAUTHORIZED)
		C=A.data.get(_S)
		if C is _E:return Response({_A:'setting_value is required'},status=status.HTTP_400_BAD_REQUEST)
		E=get_site_id(A);F=Site.objects.get(id=E);D=UserSettings.set_setting(A.user,F,B,C);return Response({_b:D.setting_name,_S:D.setting_value,_P:f"Setting {B} updated successfully"},status=status.HTTP_200_OK)
class UserProfileViewSet(viewsets.ViewSet):
	@action(detail=_C,methods=[_G])
	def current(self,request):
		A=request
		if not A.user.is_authenticated:return Response({_A:_K},status=status.HTTP_401_UNAUTHORIZED)
		try:B=UserProfile.objects.get(user=A.user)
		except UserProfile.DoesNotExist:B=UserProfile.objects.create(user=A.user)
		C=UserProfileSerializer(B,context={_D:A});return Response(C.data)
	@action(detail=_C,methods=['put','patch'])
	def update_current(self,request):
		A=request
		if not A.user.is_authenticated:return Response({_A:_K},status=status.HTTP_401_UNAUTHORIZED)
		try:C=UserProfile.objects.get(user=A.user)
		except UserProfile.DoesNotExist:C=UserProfile.objects.create(user=A.user)
		B=UserProfileSerializer(C,data=A.data,partial=_H,context={_D:A})
		if B.is_valid():B.save();return Response(B.data,status=status.HTTP_200_OK)
		return Response(B.errors,status=status.HTTP_400_BAD_REQUEST)