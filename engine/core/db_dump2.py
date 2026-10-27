_D='Successful!'
_C='value'
_B='default'
_A=None
import os,sys,datetime,decimal
from optparse import OptionParser
quote_flag=_A
def _get_table_order(app_labels):
	from django.apps import apps;from django.db.models import ForeignKey,OneToOneField;app_list=[apps.get_app_config(app_label)for app_label in app_labels]if app_labels else apps.get_apps();models={}
	for app in app_list:
		for model in app.get_models():models[model._meta.db_table]=model
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
	for(i,table)in enumerate(list(models.keys())):
		for field in models[table]._meta.fields:
			if isinstance(field,(ForeignKey,OneToOneField)):
				tname=field.related_model._meta.db_table
				if tname not in models or tname==table:continue
				rules.append((tname,table));order(s,(tname,table))
	n=[k for(k,v)in models.items()if s.count(k)==0];return[models[k]for k in s+n]
def _find_key(d,key):
	if not d:return
	for(k,v)in list(d.items()):
		if k==key:return d
		else:
			result=_find_key(v,key)
			if result is not _A:return result
def loaddb(app_labels,format,options):
	from django.db import connection,transaction
	if options.verbose:pass
	models=_get_table_order(app_labels);cursor=connection.cursor();errornum=0
	if not options.remain and not options.stdout:
		m=models[:];m.reverse()
		for model in m:
			cursor.execute(f"DELETE FROM {quote_name(model._meta.db_table)} WHERE 1=1;")
			for(table,fields)in get_model_many2many_stru(model):cursor.execute(f"DELETE FROM {quote_name(table)} WHERE 1=1;")
	success=True
	for model in models:
		try:
			load_model(cursor,model,format,options);setSequence(cursor,model)
			for(table,fields)in get_model_many2many_stru(model):load_model(cursor,(table,fields),format,options);setSequence(cursor,model)
		except Exception as e:
			import traceback;traceback.print_exc();sys.stderr.write(f"Problem loading {format} format '{model}': {str(e)}\n");success=False;errornum+=1
			if options.errorquit:transaction.rollback();raise
	if success:transaction.commit()
	else:transaction.rollback()
	if errornum:pass
	else:pass
def load_model(cursor,model,format,options):
	D='fields';C='table';B='records';A='utf-8';datadir,verbose,stdout=options.datadir,options.verbose,options.stdout;sql='INSERT INTO %s (%s) VALUES (%s);'
	if isinstance(model,(tuple,list)):filename=os.path.join(datadir,model[0]+f".{format}");fields,default=model[1],{}
	else:opts=model._meta;filename=os.path.join(datadir,opts.db_table+f".{format}");fields,default=get_model_stru(model)
	if verbose:pass
	if not os.path.exists(filename):
		if verbose:pass
		return
	try:
		objs={}
		if format=='py':
			s=[]
			with open(filename,'rb')as f:
				for line in f:
					varname=line.split(b'=')[0].decode(A)
					if varname.strip()!=B:s.append(line.decode(A))
					else:d={};exec(''.join(s),d);objs[C]=d.get(C,'');objs[D]=d.get(D,[]);objs[_B]=d.get(_B,{});objs[B]=f;break
		else:raise Exception(f"Format {format} is not supported")
		fs=objs[D];table=objs[C];default.update(objs.get(_B,{}));count=0
		for row in objs[B]:
			row=row.decode(A).strip()
			if row==']':break
			row=eval(row);d=dict(zip(fs,row));sql_fields=[];sql_values=[]
			for fd in fields:
				v=_A
				if fd in d:v=d[fd]
				elif fd in default:
					kind,value=default[fd]
					if not kind or kind==_C:v=value
					elif kind=='reference':v=d[value]
					elif kind in['date','time','datetime']:v=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				if v is not _A:sql_fields.append(fd);sql_values.append(v)
			e_sql=sql%(quote_name(table),','.join(map(quote_name,sql_fields)),','.join(['%s']*len(sql_fields)))
			if stdout:pass
			else:
				try:cursor.execute(e_sql,sql_values);count+=1
				except:sys.stderr.write(f"Error SQL: {e_sql} {sql_values}\n");raise
		if verbose:pass
	except Exception as e:import traceback;traceback.print_exc();sys.stderr.write(f"Problem loading {format} format '{filename}': {str(e)}\n");raise
def get_model_stru(model):
	from django.db.models.fields import DateField,DateTimeField,TimeField,IntegerField;fields=[];default={}
	for f in model._meta.fields:
		fields.append(f.column);v=f.get_default()
		if v is not _A:default[f.column]=_C,v
		if isinstance(f,(DateTimeField,DateField,TimeField)):
			if f.auto_now or f.auto_now_add:v=datetime.datetime.now();default[f.column]=_C,f.get_db_prep_save(v)
		if isinstance(f,IntegerField):default[f.column]=_C,_A
	return fields,default
def get_model_many2many_stru(model):
	opts=model._meta
	for f in opts.many_to_many:
		fields=[]
		if not isinstance(f.rel,GenericRel):fields.append('id');fields.append(f.m2m_column_name());fields.append(f.m2m_reverse_name());yield(f.m2m_db_table(),fields)
def dumpdb(app_labels,format,options):
	from django.apps import apps;datadir,verbose,stdout=options.datadir,options.verbose,options.stdout
	if verbose:pass
	app_list=[apps.get_app_config(app_label)for app_label in app_labels]if app_labels else apps.get_apps()
	if not os.path.exists(datadir):os.makedirs(datadir)
	errornum=0
	for app in app_list:
		for model in app.get_models():
			try:
				write_result(dump_model(model),format,options)
				for result in dump_many2many(model):write_result(result,format,options)
			except Exception as e:
				import traceback;traceback.print_exc();sys.stderr.write(f"Unable to dump database: {e}\n");errornum+=1
				if options.errorquit:raise
	if errornum:pass
	else:pass
def write_result(result,format,options):
	table=next(result);fields=next(result);filename=os.path.join(options.datadir,f"{table}.{format}")
	if options.verbose:pass
	with open(filename,'w'if not options.stdout else sys.stdout)as f:
		f.write(f"table = {repr(table)}\n");f.write(f"fields = {repr(fields)}\n");f.write('#default item format: "fieldname":("type", "value")\n');f.write('default = {}\n');f.write('records = [\n');i=0
		for t in result:f.write(f"{repr(t)},\n");i+=1
		f.write(']\n')
		if options.verbose:pass
def quote_name(s):from django.db import connection;return connection.ops.quote_name(s)
def setSequence(cursor,model):
	from django.conf import settings;from django.db.models import AutoField
	if settings.DATABASES[_B]['ENGINE']in('django.db.backends.postgresql',):
		autofields=[field for field in model._meta.fields if isinstance(field,AutoField)]
		for f in autofields:
			seq=quote_name(f"{model._meta.db_table}_{f.name}_seq");cursor.execute(f"SELECT nextval('{seq}');");nb=cursor.fetchone()[0]
			if nb:cursor.execute(f"ALTER SEQUENCE {seq} RESTART WITH {nb};")