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
	B=site_id
	if B:
		for A in MODEL_DATA:copy_initial_data(B,A[_A],A[_B],A[_C],A[_D])
def copy_initial_data(site_id,model,field_trans,field,is_translation):
	i='save complete';h='save photo complete';g='%Y%m%d-%H%M%S-%f';f=False;c='site_id';X='.';W='/';V='file_path';U='admin_id';R=True;L=model;K=site_id;D=None;j=getattr(settings,'LANGUAGES',D);S=getattr(settings,'MEDIA_ROOT',D)
	if L==_M:H=apps.get_model(_M,L)
	else:H=apps.get_model('frontend',L)
	if L==_M:
		I=MenuGroup.objects.filter(site_id=K)[:1]
		if I:I=I.get()
		B=H.objects.filter(menu_group=I)
	else:B=H.objects.filter(site_id=K)
	if not B:
		k=H.objects.filter(is_initial_data=R);Y=[]
		if k:
			Y=field_trans+field;d=[];B=H.objects.filter(is_initial_data=R)
			for E in B:d.append(E.id)
			if is_translation:
				for T in d:
					C=D
					for(Z,e)in enumerate(j):
						B=H.objects.language(e[0]).get(id=T)
						if Z==0:C=H()
						C.set_current_language(e[0]);A=getattr(B,c,D)
						if A:setattr(C,c,K)
						A=getattr(B,U,D)
						if A:setattr(C,U,A)
						N=f;M=D
						for E in Y:
							if E==_E:
								if Z==0:
									A=getattr(B,E,D)
									if A:
										O=Photo.objects.filter(object_id=B.id,content_type__model=L).values(V)[:1];J=D
										if O:
											J=O[0][V]
											if J:
												P=os.path.join(S,J)
												if os.path.exists(P):
													F=J.split(W);a=datetime.now();b=str(K)+'-'+a.strftime(g);G=F[len(F)-1].split(X)
													if len(G)>1:G=X+G[1]
													else:G=''
													F[len(F)-1]=b+G;M=W.join(F);Q=Image.open(P);Q=Q.save(os.path.join(S,M));N=R
							elif E==_R:
								if Z==0:
									A=getattr(B,E,D)
									if A:
										I=MenuGroup.objects.filter(site_id=K)
										if I:I=I.get()
							else:
								A=getattr(B,E,D)
								if A:setattr(C,E,A)
						C.save()
						if N:Photo.objects.create(content_object=C,file_path=M);print(h)
						print(i)
			else:
				print('no translation');B=H.objects.filter(is_initial_data=R);C=D;N=f
				for T in B:
					C=H();setattr(C,c,K);A=getattr(T,U,D)
					if A:setattr(C,U,A)
					for E in Y:
						if E==_E:
							print('proses photo');A=getattr(B,E,D)
							if A:
								O=Photo.objects.filter(object_id=B.id,content_type__model=L).values(V)[:1];print(_E,O);J=O[0][V]
								if J:
									P=os.path.join(S,J)
									if os.path.exists(P):
										F=J.split(W);print('file_name',F);a=datetime.now();b=str(K)+'-'+a.strftime(g);G=F[len(F)-1].split(X);print('extension',G)
										if len(G)>1:G=X+G[1]
										else:G=''
										F[len(F)-1]=b+G;M=W.join(F);Q=Image.open(P);Q=Q.save(os.path.join(S,M));N=R
						else:
							A=getattr(T,E,D)
							if A:setattr(C,E,A)
				print('begin save');C.save()
				if N:Photo.objects.create(content_object=C,file_path=M);print(h)
				print(i)