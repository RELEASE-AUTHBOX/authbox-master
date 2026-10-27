import json,os
from allauth.socialaccount.models import SocialApp
from django.core.management.base import BaseCommand
from django.db.models import OuterRef,Subquery
from menu.models import Menu,MenuTranslation
from core.auto_insert_core_data import update_core_data
from core.models import Template
from django.conf import settings
class Command(BaseCommand):
	help='Scan templates folder and save to database';template_path=settings.TEMPLATES[0]['DIRS']
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def save_template_list(A):
		C=[]
		if len(A.template_path)>0:D=A.template_path[0];C=[A for A in os.listdir(D)if os.path.isdir(os.path.join(D,A))]
		E=False;F=['allauth']
		for B in C:
			if not B in F:
				H,G=Template.objects.update_or_create(name=B,defaults={'rel_path':f"{B}/"});E=True
				if G:A.info(f"Created : {B}")
				else:A.info(f"Updated : {B}")
			else:A.info(f"Ignore : {B}")
		if E:A.info('All Done ...')
		else:A.info('Nothing To do ...')
	def handle(A,*B,**C):A.save_template_list()