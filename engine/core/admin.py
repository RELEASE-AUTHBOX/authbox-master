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
_F='updated_at'
_E='email'
_D='fields'
_C='model_list'
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
admin.site.register(Agency,TranslatableAdmin)
class BaseUserAdmin(UserAdmin):fieldsets=(None,{_D:(_E,'password')}),(_('Personal info'),{_D:(_A,_G)}),(_('Permissions'),{_D:(_H,_I,_N,_O,'user_permissions')}),(_('Important dates'),{_D:(_P,)});add_fieldsets=(None,{'classes':('wide',),_D:(_E,_A,'password1','password2',_G)}),;list_display=_E,_A,_I,_P;list_filter=_I,_N,_H,_O;search_fields=_E,_A;ordering=_E,
admin.site.register(User,BaseUserAdmin)
class ServiceAdmin(admin.ModelAdmin):list_filter=_J,;list_display=[_J,_G,_H,'site','expired_date',_F];search_fields=_J,;ordering=_B,
admin.site.register(Service,ServiceAdmin)
class TemplateAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'rel_path','get_sites',_K,_F,_L];search_fields=_A,;ordering=_B,
admin.site.register(Template,TemplateAdmin)
class TemplateOwnerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_F];search_fields=_A,;ordering=_B,
admin.site.register(TemplateOwner,TemplateOwnerAdmin)
class ModelListAdmin(admin.ModelAdmin):list_filter=_A,_Q,_L;list_display=[_A,_Q,'get_templates',_L];search_fields=_A,;ordering=_B,
admin.site.register(ModelList,ModelListAdmin)
class MenuDefaultAdmin(admin.ModelAdmin):list_filter=_K,_C;list_display=[_C,_K];search_fields=_C,;ordering=_B,
admin.site.register(MenuDefault,MenuDefaultAdmin)
class ModelListSettingAdmin(admin.ModelAdmin):list_filter=_C,_R;list_display=[_C,_R,'get_image_size',_F];search_fields=_C,;ordering=_B,
admin.site.register(ModelListSetting,ModelListSettingAdmin)
class PhotoAdmin(admin.ModelAdmin):list_filter=_M,;list_display=[_M,_F];search_fields=_M,;ordering=_B,
admin.site.register(Photo,PhotoAdmin)