_n='email_verified'
_m='avatar'
_l='images'
_k='parent_code'
_j='template_name'
_i='encrypted_template_id'
_h='value_textarea'
_g='content_type_display'
_f='value_type_display'
_e='encrypted_code'
_d='site_name'
_c='encrypted_site_id'
_b='encrypted_id'
_a='template.name'
_Z='parent.code'
_Y='value_image'
_X='get_content_type_display'
_W='get_value_type_display'
_V='site.name'
_U='last_name'
_T='first_name'
_S='email'
_R='username'
_Q='order'
_P='value_video'
_O='value_text'
_N='is_page'
_M='value_type'
_L='slug'
_K='is_active'
_J='content_type'
_I=False
_H='settings'
_G='parent'
_F='id'
_E=None
_D='request'
_C='updated_at'
_B='created_at'
_A=True
from rest_framework import serializers
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from.models import Photo,Content,SiteMetadata,Template,UserSettings,UserProfile
from.encryption import encrypt_data
User=get_user_model()
class PhotoSerializer(serializers.ModelSerializer):
	image_url=serializers.SerializerMethodField();object_id=serializers.CharField()
	class Meta:model=Photo;fields=[_F,_J,'object_id','image','image_url','title','alt_text',_B,_C];read_only_fields=[_B,_C]
	def get_image_url(C,obj):
		A=obj
		if A.image:
			B=C.context.get(_D)
			if B:return B.build_absolute_uri(A.image.url)
			return A.image.url
class TemplateSerializer(serializers.ModelSerializer):
	content_count=serializers.SerializerMethodField()
	class Meta:model=Template;fields=[_F,'name','description',_K,'content_count',_B,_C];read_only_fields=[_B,_C]
	def get_content_count(A,obj):return obj.contents.count()
class ContentSerializer(serializers.ModelSerializer):
	encrypted_id=serializers.SerializerMethodField();encrypted_site_id=serializers.SerializerMethodField();site_name=serializers.CharField(source=_V,read_only=_A);value_type_display=serializers.CharField(source=_W,read_only=_A);content_type_display=serializers.CharField(source=_X,read_only=_A);images=PhotoSerializer(source=_Y,many=_A,read_only=_A);children=serializers.SerializerMethodField();parent_code=serializers.CharField(source=_Z,read_only=_A,allow_null=_A);encrypted_template_id=serializers.SerializerMethodField();template_name=serializers.CharField(source=_a,read_only=_A,allow_null=_A);encrypted_code=serializers.SerializerMethodField();parent_id=serializers.SerializerMethodField();next_code=serializers.SerializerMethodField();image_index=serializers.SerializerMethodField()
	class Meta:model=Content;fields=[_b,_c,_d,_e,_L,'url','next_code','image_index',_M,_f,_J,_g,_N,'children',_O,_h,_P,_i,_j,'parent_id',_k,_l,_Q,_K,_B,_C];read_only_fields=[_B,_C]
	def increment_code(D,code):
		A=code.split('-');B=A[-1]
		if B.isdigit():C=int(B)+1;A.pop(-1);A.append(f"{C:02}");return'-'.join(A)
	def next_index(E,obj):
		A=Content.objects.filter(parent_id=obj.id).order_by('-code').first()
		if A:
			C=A.code;D=C.split('-');B=D[-1]
			if B.isdigit():return int(B)+1
		return 2
	def get_image_index(A,obj):B=A.next_index(obj);return B%3
	def get_next_code(C,obj):
		D=C.next_index(obj);A=obj.code;B=A.split('-');E=B[-1]
		if E.isdigit():B.pop(-1);B.append(f"{D:02}");A='-'.join(B)
		print('next_code:',A)
		if A:return encrypt_data(A)
	def get_parent_id(A,obj):
		if obj.parent:return encrypt_data(str(obj.parent.id))
	def get_encrypted_id(A,obj):return encrypt_data(str(obj.id))
	def get_encrypted_site_id(A,obj):return encrypt_data(str(obj.site_id))
	def get_encrypted_code(A,obj):return encrypt_data(obj.code)
	def get_encrypted_template_id(A,obj):return encrypt_data(str(obj.template_id))
	def get_children(A,obj):B=obj.get_children();return ContentSerializer(B,many=_A,context=A.context).data
class ContentListSerializer(serializers.ModelSerializer):
	encrypted_id=serializers.SerializerMethodField();encrypted_site_id=serializers.SerializerMethodField();site_name=serializers.CharField(source=_V,read_only=_A);value_type_display=serializers.CharField(source=_W,read_only=_A);content_type_display=serializers.CharField(source=_X,read_only=_A);parent_code=serializers.CharField(source=_Z,read_only=_A,allow_null=_A);encrypted_template_id=serializers.SerializerMethodField();template_name=serializers.CharField(source=_a,read_only=_A,allow_null=_A);images=PhotoSerializer(source=_Y,many=_A,read_only=_A);image_count=serializers.SerializerMethodField();children_count=serializers.SerializerMethodField();encrypted_code=serializers.SerializerMethodField()
	class Meta:model=Content;fields=[_b,_c,_d,_e,_L,_M,_f,_J,_g,_N,_O,_P,_i,_j,_G,_k,_l,'image_count','children_count',_Q,_K,_B,_C];read_only_fields=[_B,_C]
	def get_encrypted_id(A,obj):return encrypt_data(str(obj.id))
	def get_encrypted_site_id(A,obj):return encrypt_data(str(obj.site_id))
	def get_encrypted_code(A,obj):return encrypt_data(obj.code)
	def get_encrypted_template_id(A,obj):return encrypt_data(str(obj.template_id))
	def get_image_count(A,obj):return obj.value_image.count()
	def get_children_count(A,obj):return obj.children.filter(is_active=_A).count()
class ContentCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:model=Content;fields=['site','code',_L,'url',_M,_J,_N,_O,_h,_P,'template',_G,_Q,_K]
	def validate(E,data):
		A=data
		if _G in A and A[_G]:
			D=A[_G];B=E.instance
			if B and D.id==B.id:raise serializers.ValidationError({_G:'Content cannot be its own parent'})
			if B:
				C=D
				while C:
					if C.id==B.id:raise serializers.ValidationError({_G:'Circular parent relationship detected'})
					C=C.parent
		return A
class SiteSerializer(serializers.ModelSerializer):
	class Meta:model=Site;fields=[_F,'domain','name']
class SiteMetadataSerializer(serializers.ModelSerializer):
	site_domain=serializers.CharField(source='site.domain',read_only=_A);og_image_url=serializers.SerializerMethodField();favicon_url=serializers.SerializerMethodField();apple_touch_icon_url=serializers.SerializerMethodField();logo_url=serializers.SerializerMethodField()
	class Meta:model=SiteMetadata;fields=[_F,'site','site_domain','site_title','site_tagline','meta_description','meta_keywords','og_title','og_description','og_image','og_image_url','og_type','twitter_card','twitter_site','twitter_creator','favicon','favicon_url','apple_touch_icon','apple_touch_icon_url','logo','logo_url','theme_color','canonical_url','robots','google_site_verification','google_analytics_id','facebook_app_id',_B,_C];read_only_fields=[_B,_C]
	def get_og_image_url(C,obj):
		A=obj
		if A.og_image:
			B=C.context.get(_D)
			if B:return B.build_absolute_uri(A.og_image.url)
			return A.og_image.url
	def get_favicon_url(C,obj):
		A=obj
		if A.favicon:
			B=C.context.get(_D)
			if B:return B.build_absolute_uri(A.favicon.url)
			return A.favicon.url
	def get_apple_touch_icon_url(C,obj):
		A=obj
		if A.apple_touch_icon:
			B=C.context.get(_D)
			if B:return B.build_absolute_uri(A.apple_touch_icon.url)
			return A.apple_touch_icon.url
	def get_logo_url(C,obj):
		A=obj
		if A.logo:
			B=C.context.get(_D)
			if B:return B.build_absolute_uri(A.logo.url)
			return A.logo.url
class UserSettingsSerializer(serializers.Serializer):
	settings=serializers.DictField(child=serializers.CharField(),required=_I)
	def to_representation(F,instance):
		A=instance;from django.contrib.auth import get_user_model as G;from.common import get_site_id as H;I=G()
		if isinstance(A,I):
			C=F.context.get(_D);D=H(C)if C else _E
			if not D:return{_H:{}}
			from django.contrib.sites.models import Site;J=Site.objects.get(id=D);B=UserSettings.get_all_settings(A,J);K=UserSettings.get_default_settings()
			for(E,L)in K.items():
				if E not in B:B[E]=L
			return{_H:B}
		if isinstance(A,dict):return{_H:A}
		return{_H:{}}
	def create(C,validated_data):from.common import get_site_id as D;from django.contrib.sites.models import Site;A=C.context.get(_D);B=A.user;E=D(A);F=Site.objects.get(id=E);G=validated_data.get(_H,{});UserSettings.set_multiple_settings(B,F,G);return B
	def update(B,instance,validated_data):A=instance;from.common import get_site_id as C;from django.contrib.sites.models import Site;D=B.context.get(_D);E=C(D);F=Site.objects.get(id=E);G=validated_data.get(_H,{});UserSettings.set_multiple_settings(A,F,G);return A
class UserSerializer(serializers.ModelSerializer):
	class Meta:model=User;fields=[_F,_R,_S,_T,_U];read_only_fields=[_F]
class UserProfileSerializer(serializers.ModelSerializer):
	user=UserSerializer(read_only=_A);avatar_url=serializers.SerializerMethodField();avatar_data=PhotoSerializer(source=_m,read_only=_A);username=serializers.CharField(write_only=_A,required=_I);email=serializers.EmailField(write_only=_A,required=_I);first_name=serializers.CharField(write_only=_A,required=_I,allow_blank=_A);last_name=serializers.CharField(write_only=_A,required=_I,allow_blank=_A)
	class Meta:model=UserProfile;fields=[_F,'user',_n,_m,'avatar_data','avatar_url',_R,_S,_T,_U,_B,_C];read_only_fields=[_F,_n,_B,_C]
	def get_avatar_url(C,obj):
		A=obj
		if A.avatar and A.avatar.image:
			B=C.context.get(_D)
			if B:return B.build_absolute_uri(A.avatar.image.url)
			return A.avatar.image.url
	def update(J,instance,validated_data):
		C=instance;A=validated_data;D=A.pop(_R,_E);E=A.pop(_S,_E);F=A.pop(_T,_E);G=A.pop(_U,_E);B=C.user
		if D is not _E:B.username=D
		if E is not _E:B.email=E
		if F is not _E:B.first_name=F
		if G is not _E:B.last_name=G
		if any([D,E,F,G]):B.save()
		for(H,I)in A.items():setattr(C,H,I)
		C.save();return C