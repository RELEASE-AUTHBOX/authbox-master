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
	n='save complete';m='save photo complete';l='url';k='new_url';j='extension';i='%Y%m%d-%H%M%S-%f';h='file_name';g='proses photo';f=False;d='site_id';X='.';W='/';V='file_path';U='admin_id';Q=True;M=model;L=site_id;D=None;o=getattr(settings,'LANGUAGES',D);R=getattr(settings,'MEDIA_ROOT',D)
	if M==_M:I=apps.get_model(_M,M)
	else:I=apps.get_model('frontend',M)
	if M==_M:
		J=MenuGroup.objects.filter(site_id=L)[:1]
		if J:J=J.get()
		B=I.objects.filter(menu_group=J);
	else:B=I.objects.filter(site_id=L)
	if not B:
		Y=I.objects.filter(is_initial_data=Q);S=[]
		if Y:
			S=field_trans+field;Z=[];B=I.objects.filter(is_initial_data=Q)
			for E in B:Z.append(E.id)
			if is_translation:
				for T in Z:
					C=D
					for (a,e) in enumerate(o):
						B=I.objects.language(e[0]).get(id=T)
						if a==0:C=I();
						C.set_current_language(e[0]);A=getattr(B,d,D)
						if A:setattr(C,d,L)
						A=getattr(B,U,D)
						if A:setattr(C,U,A)
						O=f;K=D
						for E in S:
							if E==_E:
								if a==0:
									A=getattr(B,E,D)
									if A:
										N=Photo.objects.filter(object_id=B.id,content_type__model=M).values(V)[:1];H=D
										if N:H=N[0][V]
										if H:
											F=H.split(W);b=datetime.now();c=str(L)+'-'+b.strftime(i);G=F[len(F)-1].split(X);
											if len(G)>1:G=X+G[1]
											else:G=''
											F[len(F)-1]=c+G;K=W.join(F);P=Image.open(os.path.join(R,H));P=P.save(os.path.join(R,K));O=Q
							elif E==_R:
								if a==0:
									A=getattr(B,E,D)
									if A:
										J=MenuGroup.objects.filter(site_id=L)
										if J:J=J.get()
							else:
								A=getattr(B,E,D)
								if A:setattr(C,E,A)
						C.save()
						if O:Photo.objects.create(content_object=C,file_path=K);
			else:
				B=I.objects.filter(is_initial_data=Q);C=D;O=f
				for T in B:
					C=I();setattr(C,d,L);A=getattr(T,U,D)
					if A:setattr(C,U,A)
					for E in S:
						if E==_E:
							A=getattr(B,E,D)
							if A:
								N=Photo.objects.filter(object_id=B.id,content_type__model=M).values(V)[:1];H=N[0][V]
								if H:
									F=H.split(W);b=datetime.now();c=str(L)+'-'+b.strftime(i);G=F[len(F)-1].split(X);
									if len(G)>1:G=X+G[1]
									else:G=''
									F[len(F)-1]=c+G;K=W.join(F);P=Image.open(os.path.join(R,H));P=P.save(os.path.join(R,K));O=Q
						else:
							A=getattr(T,E,D)
							if A:setattr(C,E,A)
				C.save()
				if O:Photo.objects.create(content_object=C,file_path=K);