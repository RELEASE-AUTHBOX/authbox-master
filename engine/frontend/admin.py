_L='priority'
_K='order_item'
_J='link'
_I='name'
_H='sub_title'
_G='is_header_text'
_F='title'
_E='status'
_D='-updated_at'
_C='updated_at'
_B='is_initial_data'
_A='site'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from .models import *
class LogoAdmin(admin.ModelAdmin):list_filter=_A,_I;list_display=[_A,_I,_B,_C];search_fields=_A,_I;ordering=_D,
admin.site.register(Logo,LogoAdmin)
class AnnouncementAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,_L,_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Announcement,AnnouncementAdmin)
class ArticleAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Article,ArticleAdmin)
class DailyAlertAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,'alert',_J,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(DailyAlert,DailyAlertAdmin)
class DocumentAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_I,'file_path_doc',_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Document,DocumentAdmin)
class EventsAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,'location','date','time',_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Events,EventsAdmin)
class GreetingAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_I,'designation',_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Greeting,GreetingAdmin)
class NewsAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(News,NewsAdmin)
class PagesAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,'slug',_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Pages,PagesAdmin)
class PhotoGalleryAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_K,_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(PhotoGallery,PhotoGalleryAdmin)
class VideoGalleryAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_K,_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(VideoGallery,VideoGalleryAdmin)
class PopupAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_J,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Popup,PopupAdmin)
class RelatedLinkAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_I,_J,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(RelatedLink,RelatedLinkAdmin)
class SlideShowAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(SlideShow,SlideShowAdmin)
class SocialMediaAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,'kind',_J,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(SocialMedia,SocialMediaAdmin)
class TagsAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_I,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Tags,TagsAdmin)
class CategoriesAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_I,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Categories,CategoriesAdmin)
class BannerAdmin(admin.ModelAdmin):list_filter=_A,;list_display=[_A,_J,_L,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Banner,BannerAdmin)
admin.site.register(GoogleCalendar)
admin.site.register(GoogleCalendarDetail)
class WhyUsAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,'icon',_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(WhyUs,WhyUsAdmin)
class AboutUsAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(AboutUs,AboutUsAdmin)
class HowItWorksAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,_H,_K,_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(HowItWorks,HowItWorksAdmin)
class TestimonyAdmin(TranslatableAdmin):list_filter=_A,;list_display=[_A,_F,'subtitle',_G,_B,_C,_E];search_fields=_A,;ordering=_D,
admin.site.register(Testimony,TestimonyAdmin)