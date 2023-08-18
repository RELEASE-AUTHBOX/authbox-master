_D='defaults'
_C='condition'
_B='r'
_A='id'
import json,os
from allauth.socialaccount.models import SocialApp
from menu.models import Menu,MenuGroup
from .models import MenuDefault,ModelList,ModelListSetting,Template,TemplateOwner
color_done='\x1b[94m'+'DONE  '+'\x1b[0m'
def create_template_owner(file_path):
	A=[]
	with open(os.path.join(file_path,'template_owner.json'),_B)as D:A=json.load(D)
	B=1;E=len(A)
	for C in A:F=B/E*100;print(f"Writing [Template Owner] to database [%d%%]\r"%F,end='');G,H=TemplateOwner.objects.update_or_create(id=C[_C][_A],defaults=C[_D]);B+=1
	print(f"Writing [Template Owner] to database {color_done}")
def create_template(file_path):
	A=[]
	with open(os.path.join(file_path,'template.json'),_B)as D:A=json.load(D)
	B=1;E=len(A)
	for C in A:F=B/E*100;print(f"Writing [Template] to database [%d%%]\r"%F,end='');G,H=Template.objects.update_or_create(id=C[_C][_A],defaults=C[_D]);B+=1
	print(f"Writing [Template] to database {color_done}")
def create_menu(file_path):
	F='name';E='translation';C=[]
	with open(os.path.join(file_path,'menu.json'),_B)as G:C=json.load(G)
	D=1;H=len(C)
	for B in C:
		I=D/H*100;print(f"Writing [Menu] to database [%d%%]\r"%I,end='');A,L=Menu.objects.language(_A).update_or_create(id=B[_C][_A],defaults=B[_D]);A.menu_group.clear()
		for J in B['m2m']['menu_group']:K=MenuGroup.objects.get(id=J);A.menu_group.add(K)
		A.save();A.set_current_language('en');A.name=B[E][F]if B[E][F]else'';A.save();D+=1
	print(f"Writing [Menu] to database {color_done}")
def create_model_list(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list.json'),_B)as D:A=json.load(D)
	B=1;E=len(A)
	for C in A:F=B/E*100;print(f"Writing [Model List] to database [%d%%]\r"%F,end='');G,H=ModelList.objects.update_or_create(id=C[_C][_A],defaults=C[_D]);B+=1
	print(f"Writing [Model List] to database {color_done}")
def create_menu_default(file_path):
	A=[]
	with open(os.path.join(file_path,'menu_default.json'),_B)as E:A=json.load(E)
	C=1;F=len(A)
	for B in A:G=C/F*100;print(f"Writing [Menu Default] to database [%d%%]\r"%G,end='');D,H=MenuDefault.objects.update_or_create(id=B[_C][_A],defaults=B[_D]);D.service_option=B['m2m']['service_option'];D.save();C+=1
	print(f"Writing [Menu Default] to database {color_done}")
def create_model_list_setting(file_path):
	A=[]
	with open(os.path.join(file_path,'model_list_setting.json'),_B)as D:A=json.load(D)
	B=1;E=len(A);ModelListSetting.objects.all().delete()
	for C in A:F=B/E*100;print(f"Writing [Model List Setting] to database [%d%%]\r"%F,end='');G,H=ModelListSetting.objects.update_or_create(id=C[_C][_A],defaults=C[_D]);B+=1
	print(f"Writing [Model List Setting] to database {color_done}")
def create_social_app(file_path):
	A=[]
	with open(os.path.join(file_path,'social_app.json'),_B)as D:A=json.load(D)
	B=1;E=len(A)
	for C in A:F=B/E*100;print(f"Writing [Social App] to database [%d%%]\r"%F,end='');G,H=SocialApp.objects.update_or_create(id=C[_C][_A],defaults=C[_D]);B+=1
	print(f"Writing [Social App] to database {color_done}")
def create_core_data(apps,schema_monitor):A='db';create_template_owner(A);create_template(A);create_menu(A);create_model_list(A);create_menu_default(A);create_model_list_setting(A);create_social_app(A);print('ALL Done...!')
def update_core_data():A='db';create_template_owner(A);create_template(A);create_menu(A);create_model_list(A);create_menu_default(A);create_model_list_setting(A);create_social_app(A);print('ALL Data Updated...!')