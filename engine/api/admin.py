_N='is_used'
_M='user__username'
_L='email_verified'
_K='site_title'
_J='value_type'
_I='content_type'
_H='purpose'
_G='template'
_F='site'
_E='user'
_D='is_active'
_C='code'
_B='updated_at'
_A='created_at'
from django.contrib import admin
from.models import Photo,Content,Template,SiteMetadata,UserProfile,OTP
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):list_display=['id','title',_I,'object_id',_A];list_filter=[_I,_A];search_fields=['title','alt_text'];readonly_fields=[_A,_B]
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):list_display=['id','name',_D,_A];list_filter=[_D,_A];search_fields=['name','description'];readonly_fields=[_A,_B]
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):list_display=['id',_C,_J,_F,_G,_D,_A];list_filter=[_J,_D,_F,_G,_A];search_fields=[_C,'value_text'];readonly_fields=[_A,_B];raw_id_fields=['parent',_G]
@admin.register(SiteMetadata)
class SiteMetadataAdmin(admin.ModelAdmin):list_display=[_F,_K,_A,_B];search_fields=[_K,'site_tagline','meta_description'];readonly_fields=[_A,_B]
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display=[_E,_L,_A,_B];list_filter=[_L,_A];search_fields=[_M,'user__email'];readonly_fields=['email_verification_token',_A,_B]
	def get_readonly_fields(A,request,obj=None):
		if obj:return A.readonly_fields+(_E,)
		return A.readonly_fields
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
	list_display=[_E,_C,_H,_N,'is_valid_status',_A,'expires_at'];list_filter=[_H,_N,_A];search_fields=[_M,_C];readonly_fields=[_A]
	def is_valid_status(A,obj):return obj.is_valid()
	is_valid_status.boolean=True;is_valid_status.short_description='Valid'
	def get_readonly_fields(A,request,obj=None):
		if obj:return A.readonly_fields+(_E,_C,_H)
		return A.readonly_fields