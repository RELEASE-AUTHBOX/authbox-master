from core.auto_insert_core_data import update_core_data
from core.models import MenuDefault,ModelListSetting,Template
from django.core.management.base import BaseCommand
from menu.models import Menu,MenuTranslation
class Command(BaseCommand):
	help='Scan template and menu default for reference create dashboard menu'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def update_model_list_setting(D):
		E=Template.objects.all()
		for C in E:
			F=C.service_option;A=[]
			for B in F:A=list(set(A+list(MenuDefault.objects.filter(service_option__contains=B).values_list('model_list_id',flat=True))))
			for B in A:G,H=ModelListSetting.objects.update_or_create(model_list_id=B,template_id=C.id)
		D.info('All Done ...')
	def handle(A,*B,**C):A.update_model_list_setting()