_D='defaults'
_C='id'
_B='condition'
_A='r'
import json,os
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from menu.models import Menu,MenuGroup
from .models import MenuDefault,ModelList,ModelListSetting,Template,TemplateOwner
color_done='\x1b[94m'+'DONE  '+'\x1b[0m'
def create_template_owner(file_path):
	A=[]
	with open(os.path.join(file_path,'template_owner.json'),_A)as E:A=json.load(E)
	B=1;C=len(A)
	for D in A:F=B/C*100;print(f"Writing [Template Owner] to database [%d%%]\r"%F,end='');G,H=TemplateOwner.objects.update_or_create(id=D[_B][_C],defaults=D[_D]);B+=1
	print(f"Writing [Template Owner] to database ({C} data) {color_done}")
def create_template(file_path):
	A=[]
	with open(os.path.join(file_path,'template.json'),_A)as E:A=json.load(E)
	B=1;C=len(A)
	for D in A:F=B/C*100;print(f"Writing [Template] to database [%d%%]\r"%F,end='');G,H=Template.objects.update_or_create(id=D[_B][_C],defaults=D[_D]);B+=1
	print(f"Writing [Template] to database ({C} data) {color_done}")
def create_menu(file_path):
	G='name';F='translation';C=[]
	with open(os.path.join(file_path,'menu.json'),_A)as H:C=json.load(H)
	D=1;E=len(C)
	for B in C:
		I=D/E*100;print(f"Writing [Menu] to database [%d%%]\r"%I,end='');A,L=Menu.objects.language(_C).update_or_create(id=B[_B][_C],defaults=B[_D]);A.menu_group.clear()
		for J in B['m2m']['menu_group']:K=MenuGroup.objects.get(id=J);A.menu_group.add(K)
		A.save();A.set_current_language('en');A.name=B[F][G]if B[F][G]else'';A.save();D+=1
	print(f"Writing [Menu] to database ({E} data) {color_done}")
def create_model_list(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list.json'),_A)as E:A=json.load(E)
	B=1;C=len(A)
	for D in A:F=B/C*100;print(f"Writing [Model List] to database [%d%%]\r"%F,end='');G,H=ModelList.objects.update_or_create(id=D[_B][_C],defaults=D[_D]);B+=1
	print(f"Writing [Model List] to database ({C} data) {color_done}")
def create_menu_default(file_path):
	A=[]
	with open(os.path.join(file_path,'menu_default.json'),_A)as F:A=json.load(F)
	C=1;D=len(A)
	for B in A:G=C/D*100;print(f"Writing [Menu Default] to database [%d%%]\r"%G,end='');E,H=MenuDefault.objects.update_or_create(id=B[_B][_C],defaults=B[_D]);E.service_option=B['m2m']['service_option'];E.save();C+=1
	print(f"Writing [Menu Default] to database ({D} data) {color_done}")
def create_site_default(file_path):
	A=[]
	with open(os.path.join(file_path,'site_default.json'),_A)as E:A=json.load(E)
	B=1;C=len(A)
	for D in A:F=B/C*100;print(f"Writing [Site Default] to database [%d%%]\r"%F,end='');G,H=Site.objects.update_or_create(domain=D[_B]['domain'],defaults=D[_D]);B+=1
	print(f"Writing [Site Default] to database ({C} data) {color_done}")
def create_model_list_setting(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list_setting.json'),_A)as E:A=json.load(E)
	B=1;C=len(A);ModelListSetting.objects.all().delete()
	for D in A:F=B/C*100;print(f"Writing [Model List Setting] to database [%d%%]\r"%F,end='');G,H=ModelListSetting.objects.update_or_create(id=D[_B][_C],defaults=D[_D]);B+=1
	print(f"Writing [Model List Setting] to database ({C} data) {color_done}")
def create_social_app(file_path):
	A=[]
	with open(os.path.join(file_path,'social_app.json'),_A)as E:A=json.load(E)
	B=1;C=len(A)
	for D in A:F=B/C*100;print(f"Writing [Social App] to database [%d%%]\r"%F,end='');G,H=SocialApp.objects.update_or_create(id=D[_B][_C],defaults=D[_D]);B+=1
	print(f"Writing [Social App] to database ({C} data) {color_done}")
def create_core_data(apps,schema_monitor):update_core_data()
def update_core_data():A='db';create_site_default(A);create_template_owner(A);create_template(A);create_menu(A);create_model_list(A);create_menu_default(A);create_model_list_setting(A);create_social_app(A);print('ALL Data Updated...!')