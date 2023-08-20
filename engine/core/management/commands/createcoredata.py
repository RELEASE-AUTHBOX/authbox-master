_H='model_list_id'
_G='service_option'
_F=None
_E='w'
_D='defaults'
_C='condition'
_B='name'
_A='id'
import json,os
from allauth.socialaccount.models import SocialApp
from core.models import MenuDefault,ModelList,ModelListSetting,Template,TemplateOwner
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db.models import OuterRef,Subquery
from menu.models import Menu,MenuTranslation
class Command(BaseCommand):
	help='Create or Update File from database to file (This file will use in migrate process, read how to do that?)';file_path='db'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def create_template_owner(B):
		A=[];D=TemplateOwner.objects.all()
		for C in D:E={_A:C.id};F={_B:C.name};A.append({_C:E,_D:F})
		if A:
			with open(os.path.join(B.file_path,'template_owner.json'),_E)as G:G.write(json.dumps(A))
		B.info('Done Write [template_owner.json], Total files write: {}'.format(len(A)))
	def create_template(C):
		B=[];D=Template.objects.all()
		for A in D:E={_A:A.id};F={_B:A.name,'rel_path':A.rel_path,'is_frontend':A.is_frontend,'template_owner_id':A.template_owner.id if A.template_owner else _F,_G:A.service_option};B.append({_C:E,_D:F})
		if B:
			with open(os.path.join(C.file_path,'template.json'),_E)as G:G.write(json.dumps(B))
		C.info('Done Write [template.json], Total files write: {}'.format(len(B)))
	def create_menu(C):
		B=[];E=Subquery(MenuTranslation.objects.filter(master_id=OuterRef(_A),language_code='en').values(_B));F=Menu.objects.language(_A).filter(kind=2).annotate(name_en=E)
		for A in F:
			G={_A:A.id};H={_B:A.name,'parent_id':A.parent.id if A.parent else _F,'link':A.link,'order_menu':A.order_menu,'icon':A.icon,'kind':A.kind,'is_visibled':A.is_visibled,'is_external':A.is_external,'is_new':A.is_new,'exclude_menu':A.exclude_menu};I={_B:A.name_en};D=[]
			for J in A.menu_group.all():D.append(J.id)
			K={'menu_group':D};B.append({_C:G,_D:H,'translation':I,'m2m':K})
		if B:
			with open(os.path.join(C.file_path,'menu.json'),_E)as L:L.write(json.dumps(B))
		C.info('Done Write [menu.json], Total files write: {}'.format(len(B)))
	def create_model_list(C):
		B=[];D=ModelList.objects.all()
		for A in D:E={_A:A.id};F={_B:A.name,'description':A.description,'menu_id':A.menu.id if A.menu else _F,'status':A.status};B.append({_C:E,_D:F})
		if B:
			with open(os.path.join(C.file_path,'model_list.json'),_E)as G:G.write(json.dumps(B))
		C.info('Done Write [model_list.json], Total files write: {}'.format(len(B)))
	def convert_to_list(C,data):
		A=[]
		for B in data:A.append(int(B))
		return A
	def create_menu_default(B):
		A=[];D=MenuDefault.objects.all()
		for C in D:E={_G:B.convert_to_list(C.service_option)};F={_A:C.id};G={_H:C.model_list.id};A.append({_C:F,_D:G,'m2m':E})
		if A:
			with open(os.path.join(B.file_path,'menu_default.json'),_E)as H:H.write(json.dumps(A))
		B.info('Done Write [menu_default.json], Total files write: {}'.format(len(A)))
	def create_site_default(B):
		A=[];D=Site.objects.filter(domain__in=['localhost:8000','127.0.0.1:8000'])
		for C in D:E={'domain':C.domain};F={_B:C.name};A.append({_C:E,_D:F})
		if A:
			with open(os.path.join(B.file_path,'site_default.json'),_E)as G:G.write(json.dumps(A))
		B.info('Done Write [site_default.json], Total files write: {}'.format(len(A)))
	def create_model_list_setting(C):
		B=[];D=ModelListSetting.objects.all()
		for A in D:E={_A:A.id};F={_H:A.model_list.id if A.model_list else _F,'template_id':A.template.id if A.template else _F,'image_width':A.image_width,'image_height':A.image_height};B.append({_C:E,_D:F})
		if B:
			with open(os.path.join(C.file_path,'model_list_setting.json'),_E)as G:G.write(json.dumps(B))
		C.info('Done Write [model_list_setting.json], Total files write: {}'.format(len(B)))
	def create_social_app(C):
		B=[];D=SocialApp.objects.all()
		for A in D:E={_A:A.id};F={'provider':A.provider,_B:A.name,'client_id':A.client_id,'secret':A.secret,'key':A.key};B.append({_C:E,_D:F})
		if B:
			with open(os.path.join(C.file_path,'social_app.json'),_E)as G:G.write(json.dumps(B))
		C.info('Done Write [social_app.json], Total files write: {}'.format(len(B)))
	def handle(A,*B,**C):A.create_site_default();A.create_template_owner();A.create_template();A.create_menu();A.create_model_list();A.create_menu_default();A.create_model_list_setting();A.create_social_app();A.info('All Done ...')