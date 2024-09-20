import sys
from django.core.management.base import BaseCommand
from django.apps import apps
from core.db_dump2 import _get_table_order
class Command(BaseCommand):
	help='Migrate All Data From sqlite3 to mysql'
	def info(A,message):sys.stdout.write(message)
	def debug(A,message):sys.stdout.write(message)
	def do_migrate(A):
		B='core';A.info('Begin Migrate ...\n');
		for C in apps.all_models[B]:A.info('Proses '+C);D=apps.get_model(B,C)
		A.info('All Done ...')
	def handle(A,*B,**C):A.do_migrate()