from core.auto_insert_core_data import update_core_data
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Load data from file to database';file_path='db'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def handle(A,*B,**C):update_core_data()