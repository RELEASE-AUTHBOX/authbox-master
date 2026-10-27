from django.db import connections
from django.core.management.base import BaseCommand
class Command(BaseCommand):
	help='Scan template and menu default for reference create dashboard menu'
	def info(A,message):A.stdout.write(message)
	def debug(A,message):A.stdout.write(message)
	def migrate_to_wordpress(B):
		A=connections['second_db'].cursor();A.execute('SELECT * FROM lobar_posts');C=A.fetchall()[:1]
		for D in C:pass
		B.info('All Done ...')
	def handle(A,*B,**C):A.migrate_to_wordpress()