_J='select %s from %s'
_I='(Total %d records)\n'
_H='%Y-%m-%d %H:%M:%S'
_G='%H:%M:%S'
_F='%Y-%m-%d'
_E='Successful!'
_D="Problem loading %s format '%s' : %s\n"
_C='.%s'
_B='value'
_A=None
import os,sys,datetime,decimal
from optparse import OptionParser
quote_flag=_A
def _get_table_order(app_labels):
	from django.db.models import get_app,get_apps,get_models,ForeignKey,OneToOneField
	if not app_labels:app_list=get_apps()
	else:app_list=[get_app(app_label)for app_label in app_labels]
	models={}
	for app in app_list:
		for model in get_models(app):models[model._meta.db_table]=model
	s=[];rules=[]
	def order(s,rule):
		a,b=rule
		try:
			i=s.index(a)
			try:
				j=s.index(b)
				if j<i:del s[i];s.insert(j,a)
			except:s.append(b)
		except:
			s.append(a)
			try:j=s.index(b);del s[j];s.append(b)
			except:s.append(b)
	for(i,table)in enumerate(models.keys()[:]):
		for field in models[table]._meta.fields:
			if isinstance(field,(ForeignKey,OneToOneField)):
				tname=field.rel.to._meta.db_table
				if not models.has_key(tname)or tname==table:continue
				rules.append((tname,table));order(s,(tname,table))
	n=[]
	for(k,v)in models.items():
		if s.count(k)==0:n.append(k)
	return[models[k]for k in s+n]
def _find_key(d,key):
	if not d:return
	for(k,v)in d.items()[:]:
		if k==key:return d
		else:
			result=_find_key(v,key)
			if result is not _A:return result
def loaddb(app_labels,format,options):
	A='DELETE FROM %s WHERE 1=1;';from django.db import connection,transaction
	if options.verbose:pass
	models=_get_table_order(app_labels);cursor=connection.cursor();errornum=0
	if not options.remain and not options.stdout:
		m=models[:];m.reverse()
		for model in m:
			cursor.execute(A%quote_name(model._meta.db_table))
			for(table,fields)in get_model_many2many_stru(model):cursor.execute(A%quote_name(table))
	success=True
	for model in models:
		try:
			load_model(cursor,model,format,options);setSequence(cursor,model)
			for(table,fields)in get_model_many2many_stru(model):load_model(cursor,(table,fields),format,options);setSequence(cursor,model)
		except Exception(e):
			import traceback;traceback.print_exc();sys.stderr.write(_D%(format,model,str(e)));success=False;errornum+=1
			if options.errorquit:transaction.rollback_unless_managed();raise
	if success:transaction.commit_unless_managed()
	else:transaction.rollback_unless_managed()
	if errornum:pass
	else:pass
def load_model(cursor,model,format,options):
	E='now';D='default';C='fields';B='table';A='records';datadir,verbose,stdout=options.datadir,options.verbose,options.stdout;sql='INSERT INTO %s (%s) VALUES (%s);'
	if isinstance(model,(tuple,list)):filename=os.path.join(datadir,model[0]+_C%format);fields,default=model[1],{}
	else:opts=model._meta;filename=os.path.join(datadir,opts.db_table+_C%format);fields,default=get_model_stru(model)
	if verbose:pass
	if not os.path.exists(filename):
		if verbose:pass
		return
	try:
		objs={}
		if format=='py':
			s=[];f=file(filename,'rb')
			for line in f:
				varname=line.split('=')[0]
				if varname.strip()!=A:s.append(line)
				else:d={};exec(''.join(s)in d);objs[B]=d.get(B,'');objs[C]=d.get(C,[]);objs[D]=d.get(D,{});objs[A]=f;break
		else:raise'Not support this format %s'%format
		fs=objs[C];table=objs[B];default.update(objs.get(D,{}));count=0
		for row in objs[A]:
			if row.strip()==']':break
			row=eval(row);d=dict(zip(fs,row));sql_fields=[];sql_values=[]
			for fd in fields:
				v=_A
				if d.has_key(fd):v=d[fd]
				elif default.get(fd,_A)is not _A:
					kind,value=default[fd]
					if not kind or kind==_B:v=value
					elif kind=='reference':
						try:v=d[value]
						except KeyError:sys.stderr.write('Referenced field [%s] does not exist\n'%value);raise
					elif kind=='date':
						if not value or value==E:v=datetime.date.today().strftime(_F)
						else:v=value
					elif kind=='time':
						if not value or value==E:v=datetime.datetime.now().strftime(_G)
						else:v=value
					elif kind=='datetime':
						if not value or value==E:v=datetime.datetime.now().strftime(_H)
						else:v=value
					else:raise Exception("Cann't support this default type [%s]\n"%kind)
				if v is not _A:sql_fields.append(fd);sql_values.append(v)
			e_sql=sql%(quote_name(table),','.join(map(quote_name,sql_fields)),','.join(['%s']*len(sql_fields)))
			if stdout:pass
			else:
				try:cursor.execute(e_sql,sql_values);count+=1
				except:sys.stderr.write('Error sql: %s %s\n'%(e_sql,sql_values));raise
		if verbose:pass
	except Exception(e):import traceback;traceback.print_exc();sys.stderr.write(_D%(format,filename,str(e)));raise
def get_model_stru(model):
	from django.db.models.fields import DateField,DateTimeField,TimeField,IntegerField;fields=[];default={}
	for f in model._meta.fields:
		fields.append(f.column);v=f.get_default()
		if v is not _A:default[f.column]=_B,v
		if isinstance(f,(DateTimeField,DateField,TimeField)):
			if f.auto_now or f.auto_now_add:v=datetime.datetime.now();default[f.column]=_B,f.get_db_prep_save(v)
		if isinstance(f,IntegerField):default[f.column]=_B,_A
	return fields,default
def get_model_many2many_stru(model):
	try:from django.db.models import GenericRel
	except:from django.contrib.contenttypes.generic import GenericRel
	opts=model._meta
	for f in opts.many_to_many:
		fields=[]
		if not isinstance(f.rel,GenericRel):fields.append('id');fields.append(f.m2m_column_name());fields.append(f.m2m_reverse_name());yield(f.m2m_db_table(),fields)
def dumpdb(app_labels,format,options):
	from django.db.models import get_app,get_apps,get_models;datadir,verbose,stdout=options.datadir,options.verbose,options.stdout
	if verbose:pass
	if len(app_labels)==0:app_list=get_apps()
	else:app_list=[get_app(app_label)for app_label in app_labels]
	if not os.path.exists(datadir):os.makedirs(datadir)
	errornum=0
	for app in app_list:
		for model in get_models(app):
			try:
				write_result(dump_model(model),format,options)
				for result in dump_many2many(model):write_result(result,format,options)
			except Exception(e):
				import traceback;traceback.print_exc();sys.stderr.write('Unable to dump database: %s\n'%e);errornum+=1
				if options.errorquit:raise
	if errornum:pass
	else:pass
def dump_model(model):from django.db import connection;opts=model._meta;cursor=connection.cursor();fields,default=get_model_stru(model);cursor.execute(_J%(','.join(map(quote_name,fields)),quote_name(opts.db_table)));return call_cursor(opts.db_table,fields,cursor)
def call_cursor(table,fields,cursor):
	yield table;yield fields
	while 1:
		rows=cursor.fetchmany(100)
		if rows:
			for row in rows:yield _pre_data(row)
		else:break
def _pre_data(row):
	row=list(row)
	for(i,fd)in enumerate(row):
		if isinstance(fd,datetime.datetime):row[i]=row[i].strftime(_H)
		elif isinstance(fd,datetime.date):row[i]=row[i].strftime(_F)
		elif isinstance(fd,datetime.time):row[i]=row[i].strftime(_G)
		elif isinstance(fd,decimal.Decimal):row[i]=row[i].__float__()
	return row
def dump_many2many(model):
	from django.db import connection;cursor=connection.cursor()
	for(table,fields)in get_model_many2many_stru(model):cursor.execute(_J%(','.join(map(quote_name,fields)),quote_name(table)));yield call_cursor(table,fields,cursor)
def write_result(result,format,options):
	table=result.next();fields=result.next();filename=os.path.join(options.datadir,table+_C%format)
	if options.verbose:pass
	if not options.stdout:f=file(filename,'wb')
	else:f=sys.stdout
	print>>f,'table = %r'%table;print>>f,'fields = %r'%fields;print>>f,'#default item format: "fieldname":("type", "value")';print>>f,'default = {}';print>>f,'records = [';i=0
	for t in result:print>>f,repr(t);i+=1
	print>>f,']'
	if options.verbose:pass
	if not options.stdout:f.close()
def quote_name(s):
	from django.db import backend
	if quote_flag=='old':return backend.quote_name(s)
	else:return backend.DatabaseOperations().quote_name(s)
def setSequence(cursor,model):
	from django.conf import settings;from django.db.models import AutoField
	if settings.DATABASE_ENGINE in('postgresql_psycopg2','postgresql'):
		autofields=[field for field in model._meta.fields if isinstance(field,AutoField)]
		for f in autofields:
			seq=quote_name('%s_%s_seq'%(model._meta.db_table,f.name));cursor.execute("SELECT nextval('%s');"%seq);nb=cursor.fetchall()[0][0]
			if nb:cursor.execute('ALTER SEQUENCE %s RESTART WITH %d;'%(seq,nb))
def get_usage():usage='\n  %prog [options] action [applist]:\n      action: dump load\n';return usage
def execute_from_command_line(argv=_A):
	B='datadir';A='store_true'
	if argv is _A:argv=sys.argv
	parser=OptionParser(usage=get_usage());parser.add_option('--settings',help='Python path to settings module, e.g. "myproject.settings.main". If this isn\'t provided, the DJANGO_SETTINGS_MODULE environment variable will be used.');parser.add_option('-d','--dir',help='Output/Input directory.',default=B,dest=B);parser.add_option('-v','--verbose',help='Verbose mode',action=A);parser.add_option('-s','--stdout',help='Output the data to stdout',action=A);parser.add_option('-r','--remain',help='Remain the records of the tables, default will delete all the records. Only used for loading.',action=A);parser.add_option('-e','--errorquit',help='If there are errors occured, then exit the program.',action=A);options,args=parser.parse_args(argv[1:])
	if len(args)==0:parser.print_help();sys.exit(0)
	action=args[0];apps=args[1:]
	if options.settings:os.environ['DJANGO_SETTINGS_MODULE']=options.settings
	else:
		from django.core.management import setup_environ
		try:import settings
		except ImportError:sys.exit()
		setup_environ(settings)
	global quote_flag;import django.db
	try:django.db.backend.quote_name;quote_flag='old'
	except AttributeError:quote_flag='new'
	if action=='dump':dumpdb(apps,'py',options)
	elif action=='load':loaddb(apps,'py',options)
	else:parser.print_help()
if __name__=='__main__':execute_from_command_line()