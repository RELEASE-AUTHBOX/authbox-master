_U='Photo (OG Image)'
_T='position'
_S='model_list_setting'
_R='last_login'
_Q='groups'
_P='is_superuser'
_O='template'
_N='service_option'
_M='kind'
_L='is_staff'
_K='is_active'
_J='file_path'
_I='status'
_H='description'
_G='agency'
_F='email'
_E='fields'
_D='model_list'
_C='updated_at'
_B='-updated_at'
_A='name'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from.models import*
from.forms import*
from django.contrib.auth import get_user_model
User=get_user_model()
class AgencyAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,'shortuuid','province','regency','sub_district','urban_village','address','phone',_C];search_fields=_A,;ordering=_B,
admin.site.register(Agency,AgencyAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_E:(_F,'password')}),(_('Personal info'),{_E:(_A,_G)}),(_('Permissions'),{_E:(_K,_L,_P,_Q,'user_permissions')}),(_('Important dates'),{_E:(_R,)});add_fieldsets=(None,{'classes':('wide',),_E:(_F,_A,'password1','password2',_G)}),;list_display=_F,_A,_L,_R;list_filter=_L,_P,_K,_Q;search_fields=_F,_A;ordering=_F,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_G,_M;list_display=[_G,_M,_K,'site','expired_date',_C];search_fields=_G,_M;ordering=_B,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path','get_sites',_N,'template_owner',_C,_I];search_fields=_A,;ordering=_B,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_C];search_fields=_A,;ordering=_B,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_H,_I;list_display=[_A,_H,'get_templates',_I];search_fields=_A,;ordering=_B,
admin.site.register(ModelList,ModelListAdmin)
class MenuDefaultAdmin(admin.ModelAdmin):list_filter=_N,_D;list_display=[_D,_N];search_fields=_D,;ordering=_B,
admin.site.register(MenuDefault,MenuDefaultAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_D,_O;list_display=[_D,_O,_C];search_fields=_D,;ordering=_B,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class ImageDimensionAdmin(admin.ModelAdmin):list_filter=_S,_T;list_display=['get_model_list_name',_T,'get_image_size'];search_fields=_S,
admin.site.register(ImageDimension,ImageDimensionAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_J,;list_display=['content_type',_J,'object_id','content_object',_C];search_fields=_J,;ordering=_B,
admin.site.register(Photo,PhotoAdmin)
class GlobalSettingAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'value','site','order_item',_C];search_fields=_A,;ordering=_B,
admin.site.register(GlobalSetting,GlobalSettingAdmin)
class TemplateBlockAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_O,'id',_A,'price_level',_H,_I,_C];search_fields=_A,;ordering=_B,
admin.site.register(TemplateBlock,TemplateBlockAdmin)
class AgencyMetaPhotoInline(GenericTabularInline):model=Photo;extra=1;max_num=1;verbose_name=_U;verbose_name_plural=_U;fields=[_J,_H]
class AgencyMetaAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'id','url','title',_H,'web_type',_C];search_fields=_A,;ordering=_B,;inlines=[AgencyMetaPhotoInline]
admin.site.register(AgencyMeta,AgencyMetaAdmin)