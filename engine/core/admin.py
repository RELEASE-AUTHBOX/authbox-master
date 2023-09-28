_R='template'
_Q='description'
_P='last_login'
_O='groups'
_N='is_superuser'
_M='file_path'
_L='status'
_K='service_option'
_J='kind'
_I='is_staff'
_H='is_active'
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
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_E:(_F,'password')}),(_('Personal info'),{_E:(_A,_G)}),(_('Permissions'),{_E:(_H,_I,_N,_O,'user_permissions')}),(_('Important dates'),{_E:(_P,)});add_fieldsets=(None,{'classes':('wide',),_E:(_F,_A,'password1','password2',_G)}),;list_display=_F,_A,_I,_P;list_filter=_I,_N,_H,_O;search_fields=_F,_A;ordering=_F,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_G,_J;list_display=[_G,_J,_H,'site','expired_date',_C];search_fields=_G,_J;ordering=_B,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path','get_sites',_K,'template_owner',_C,_L];search_fields=_A,;ordering=_B,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_C];search_fields=_A,;ordering=_B,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_Q,_L;list_display=[_A,_Q,'get_templates',_L];search_fields=_A,;ordering=_B,
admin.site.register(ModelList,ModelListAdmin)
class MenuDefaultAdmin(admin.ModelAdmin):list_filter=_K,_D;list_display=[_D,_K];search_fields=_D,;ordering=_B,
admin.site.register(MenuDefault,MenuDefaultAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_D,_R;list_display=[_D,_R,'get_image_size',_C];search_fields=_D,;ordering=_B,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_M,;list_display=['content_type',_M,'object_id','content_object',_C];search_fields=_M,;ordering=_B,
admin.site.register(Photo,PhotoAdmin)