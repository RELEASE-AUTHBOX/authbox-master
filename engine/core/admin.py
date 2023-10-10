_R='description'
_Q='last_login'
_P='groups'
_O='is_superuser'
_N='file_path'
_M='template'
_L='service_option'
_K='kind'
_J='is_staff'
_I='is_active'
_H='status'
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
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
User=get_user_model()
class AgencyAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,'shortuuid','province','regency','sub_district','urban_village','address','phone',_C];search_fields=_A,;ordering=_B,
admin.site.register(Agency,AgencyAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_E:(_F,'password')}),(_('Personal info'),{_E:(_A,_G)}),(_('Permissions'),{_E:(_I,_J,_O,_P,'user_permissions')}),(_('Important dates'),{_E:(_Q,)});add_fieldsets=(None,{'classes':('wide',),_E:(_F,_A,'password1','password2',_G)}),;list_display=_F,_A,_J,_Q;list_filter=_J,_O,_I,_P;search_fields=_F,_A;ordering=_F,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_G,_K;list_display=[_G,_K,_I,'site','expired_date',_C];search_fields=_G,_K;ordering=_B,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path','get_sites',_L,'template_owner',_C,_H];search_fields=_A,;ordering=_B,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_C];search_fields=_A,;ordering=_B,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_R,_H;list_display=[_A,_R,'get_templates',_H];search_fields=_A,;ordering=_B,
admin.site.register(ModelList,ModelListAdmin)
class MenuDefaultAdmin(admin.ModelAdmin):list_filter=_L,_D;list_display=[_D,_L];search_fields=_D,;ordering=_B,
admin.site.register(MenuDefault,MenuDefaultAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_D,_M;list_display=[_D,_M,'get_image_size',_C];search_fields=_D,;ordering=_B,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_N,;list_display=['content_type',_N,'object_id','content_object',_C];search_fields=_N,;ordering=_B,
admin.site.register(Photo,PhotoAdmin)
class GlobalSettingAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'value','site',_C];search_fields=_A,;ordering=_B,
admin.site.register(GlobalSetting,GlobalSettingAdmin)
class TemplateBlockAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_M,_A,'variation','price_level',_H,_C];search_fields=_A,;ordering=_B,
admin.site.register(TemplateBlock,TemplateBlockAdmin)