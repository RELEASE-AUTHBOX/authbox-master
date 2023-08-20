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
_F='fields'
_E='model_list'
_D='updated_at'
_C='email'
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
class AgencyAdmin(TranslatableAdmin):list_filter=_A,_C;list_display=[_A,'shortuuid','province','regency','sub_district','urban_village','address','phone','notes',_D];search_fields=_A,_C;ordering=_B,
admin.site.register(Agency,AgencyAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_F:(_C,'password')}),(_('Personal info'),{_F:(_A,_G)}),(_('Permissions'),{_F:(_H,_I,_N,_O,'user_permissions')}),(_('Important dates'),{_F:(_P,)});add_fieldsets=(None,{'classes':('wide',),_F:(_C,_A,'password1','password2',_G)}),;list_display=_C,_A,_I,_P;list_filter=_I,_N,_H,_O;search_fields=_C,_A;ordering=_C,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_J,;list_display=[_J,_G,_H,'site','expired_date',_D];search_fields=_J,;ordering=_B,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path','get_sites',_K,_D,_L];search_fields=_A,;ordering=_B,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_D];search_fields=_A,;ordering=_B,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_Q,_L;list_display=[_A,_Q,'get_templates',_L];search_fields=_A,;ordering=_B,
admin.site.register(ModelList,ModelListAdmin)
class MenuDefaultAdmin(admin.ModelAdmin):list_filter=_K,_E;list_display=[_E,_K];search_fields=_E,;ordering=_B,
admin.site.register(MenuDefault,MenuDefaultAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_E,_R;list_display=[_E,_R,'get_image_size',_D];search_fields=_E,;ordering=_B,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_M,;list_display=[_M,_D];search_fields=_M,;ordering=_B,
admin.site.register(Photo,PhotoAdmin)