_C='get_crop_image_size'
_B='upload_photo'
_A='post_login_redirect'
from django.urls import path
from backend.views import PostLoginView
from .views import *
from core.payment import payment
urlpatterns=[path('dashboard/upload-photo/<int:width>/<int:height>/',upload_photo,name=_B),path('dashboard/upload-photo/<int:width>/<int:height>/<int:save_as_png>/',upload_photo,name=_B),path('pre-login/',pre_login,name='pre_login'),path('post-login/',PostLoginView.as_view(),name='post_login'),path('post-login/redirect/',post_login_redirect,name=_A),path('post-login/redirect/<uuid:uuid>/',post_login_redirect,name=_A),path('post-login/redirect/<int:user_id>/<uuid:uuid>/',post_login_redirect,name=_A),path('login-social-media/<str:social_media>/<int:site_id>/',redirect_to_main,name='redirect_to_main'),path('social-media/<int:user_id>/<uuid:uuid>/',social_media,name='social_media'),path('force-authenticate-out/',force_authenticate_out,name='force_authenticate_out'),path('get-crop-image-size/<str:model_name>/',get_crop_image_size,name=_C),path('get-crop-image-size/<str:model_name>/<int:position>/',get_crop_image_size,name=_C),path('account_activation_sent/',account_activation_sent,name='account_activation_sent'),path('activate/<str:uidb64>/<str:token>/',activate,name='activate'),path('payment/<str:order_id>/<int:gross_amount>/<str:user_email>/',payment,name='payment')]