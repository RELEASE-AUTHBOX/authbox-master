_R='menu_group'
_Q='subtitle'
_P='location'
_O='priority'
_N='icon'
_M='menu'
_L='order_item'
_K='link'
_J='name'
_I='sub_title'
_H='content'
_G='is_header_text'
_F='title'
_E='photo'
_D='is_translation'
_C='field'
_B='field_trans'
_A='model'
from django.db import transaction
import os
from menu.models import Menu,MenuGroup
from datetime import datetime
from django.apps import apps
from django.conf import settings
from core.models import Photo
from PIL import Image
MODEL_DATA=[{_A:'logo',_B:[_J],_C:[_E],_D:0},{_A:'favicon',_B:[_J],_C:[_E],_D:0},{_A:'tags',_B:[_J],_C:[],_D:1},{_A:'categories',_B:[_J],_C:[],_D:1},{_A:'announcement',_B:[_F,_I,_H],_C:[_G,_O,_E],_D:1},{_A:'news',_B:[_F,_I,_H],_C:[_G,_E],_D:1},{_A:'article',_B:[_F,_I,_H],_C:[_G,_E],_D:1},{_A:'events',_B:[_F,_I,_H,_P],_C:[_G,'date','time',_E],_D:1},{_A:'slideshow',_B:[_F,_I,_H],_C:[_E],_D:1},{_A:'dailyalert',_B:['alert'],_C:[_K],_D:1},{_A:'whyus',_B:[_F,_I,'description'],_C:[_G],_D:1},{_A:'greeting',_B:[_F,_H,_J,'designation'],_C:[_E],_D:1},{_A:'socialmedia',_B:['kind',_K],_C:[],_D:0},{_A:'photogallery',_B:[_F,_H],_C:[_G,_L,_E],_D:1},{_A:'fasilities',_B:[_F,_I,_H],_C:[_G,_L,_E],_D:1},{_A:'offers',_B:[_F,_I,_H],_C:[_G,_L,_E],_D:1},{_A:'howitworks',_B:[_F,_I,_H],_C:[_N,_G,_L,_E],_D:1},{_A:'aboutus',_B:[_F,_I,_H],_C:[_G,_E],_D:1},{_A:'testimony',_B:[_H],_C:[_F,_Q,_G,_E],_D:1},{_A:'product',_B:[_J,_F,_I,_H],_C:[_G,_L,_N,'price',_E],_D:1},{_A:'videogallery',_B:[_F],_C:['embed','embed_video',_G,_L,_E],_D:1},{_A:'relatedlink',_B:[_J],_C:[_K],_D:1},{_A:'document',_B:[_J,_H],_C:[_G,_E],_D:1},{_A:'popup',_B:[_F],_C:[_K,_E],_D:1},{_A:'banner',_B:[_K,_O],_C:[_E],_D:0},{_A:_P,_B:[_F,_Q],_C:['embed',_G],_D:1},{_A:_M,_B:[_J],_C:[_R,'parent',_K,'order_menu',_N,'kind','is_visibled','is_external','is_new','exclude_menu'],_D:1},{_A:'pages',_B:[_F,_I,_H],_C:[_M,_G,_E],_D:1}]
@transaction.atomic
def do_init_data(site_id):
	for A in MODEL_DATA:copy_initial_data(site_id,A[_A],A[_B],A[_C],A[_D])
def copy_initial_data(site_id,model,field_trans,field,is_translation):
	m='save complete';l='save photo complete';k='url';j='new_url';i='extension';h='%Y%m%d-%H%M%S-%f';g='file_name';f='proses photo';d='site_id';X='.';W='/';V='file_path';U='admin_id';P=True;M=model;L=site_id;G=None;n=getattr(settings,'LANGUAGES',G);Q=getattr(settings,'MEDIA_ROOT',G)
	if M==_M:H=apps.get_model(_M,M)
	else:H=apps.get_model('frontend',M)
	print('---------------------');print('proses',M)
	if M==_M:
		J=MenuGroup.objects.filter(site_id=L)[:1]
		if J:J=J.get()
		B=H.objects.filter(menu_group=J);print(';menu',B)
	else:B=H.objects.filter(site_id=L)
	if not B:
		print('model kosong (lanjutkan)',B);Y=H.objects.filter(is_initial_data=P);print('src_data',Y);R=[]
		if Y:
			print('data initial data ',Y);R=field_trans+field;print('mfield_all',R);Z=[];B=H.objects.filter(is_initial_data=P)
			for D in B:Z.append(D.id)
			print('m_array',Z)
			if is_translation:
				for S in Z:
					C=G
					for (a,e) in enumerate(n):
						B=H.objects.language(e[0]).get(id=S)
						if a==0:C=H();print('obj_create')
						C.set_current_language(e[0]);A=getattr(B,d,G)
						if A:setattr(C,d,L)
						A=getattr(B,U,G)
						if A:setattr(C,U,A)
						T=False;K=G
						for D in R:
							if D==_E:
								if a==0:
									print(f);A=getattr(B,D,G)
									if A:
										N=Photo.objects.filter(object_id=B.id,content_type__model=M).values(V)[:1];print(_E,N);I=N[0][V]
										if I:
											E=I.split(W);print(g,E);b=datetime.now();c=str(L)+'-'+b.strftime(h);F=E[len(E)-1].split(X);print(i,F)
											if len(F)>1:F=X+F[1]
											else:F=''
											E[len(E)-1]=c+F;K=W.join(E);print(j,K);print(k,I);O=Image.open(os.path.join(Q,I));O=O.save(os.path.join(Q,K));T=P
							elif D==_R:
								if a==0:
									print('proses menu_group');A=getattr(B,D,G)
									if A:
										J=MenuGroup.objects.filter(site_id=L)
										if J:J=J.get()
							else:
								A=getattr(B,D,G)
								if A:setattr(C,D,A)
						C.save()
						if T:Photo.objects.create(content_object=C,file_path=K);print(l)
						print(m)
			else:
				print('no translation');B=H.objects.filter(is_initial_data=P);C=G
				for S in B:
					C=H();setattr(C,d,L);A=getattr(S,U,G)
					if A:setattr(C,U,A)
					for D in R:
						if D==_E:
							print(f);A=getattr(B,D,G)
							if A:
								N=Photo.objects.filter(object_id=B.id,content_type__model=M).values(V)[:1];print(_E,N);I=N[0][V]
								if I:
									E=I.split(W);print(g,E);b=datetime.now();c=str(L)+'-'+b.strftime(h);F=E[len(E)-1].split(X);print(i,F)
									if len(F)>1:F=X+F[1]
									else:F=''
									E[len(E)-1]=c+F;K=W.join(E);print(j,K);print(k,I);O=Image.open(os.path.join(Q,I));O=O.save(os.path.join(Q,K));T=P
						else:
							A=getattr(S,D,G)
							if A:setattr(C,D,A)
				print('begin save');C.save()
				if T:Photo.objects.create(content_object=C,file_path=K);print(l)
				print(m)