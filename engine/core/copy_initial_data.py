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
	h='save complete';g='save photo complete';f='%Y%m%d-%H%M%S-%f';e=False;b='site_id';W='.';V='/';U='file_path';T='admin_id';Q=True;M=model;K=site_id;D=None;i=getattr(settings,'LANGUAGES',D);R=getattr(settings,'MEDIA_ROOT',D)
	if M==_M:H=apps.get_model(_M,M)
	else:H=apps.get_model('frontend',M)
	if M==_M:
		J=MenuGroup.objects.filter(site_id=K)[:1]
		if J:J=J.get()
		B=H.objects.filter(menu_group=J)
	else:B=H.objects.filter(site_id=K)
	if not B:
		j=H.objects.filter(is_initial_data=Q);X=[]
		if j:
			X=field_trans+field;c=[];B=H.objects.filter(is_initial_data=Q)
			for E in B:c.append(E.id)
			if is_translation:
				for S in c:
					C=D
					for (Y,d) in enumerate(i):
						B=H.objects.language(d[0]).get(id=S)
						if Y==0:C=H()
						C.set_current_language(d[0]);A=getattr(B,b,D)
						if A:setattr(C,b,K)
						A=getattr(B,T,D)
						if A:setattr(C,T,A)
						N=e;L=D
						for E in X:
							if E==_E:
								if Y==0:
									A=getattr(B,E,D)
									if A:
										O=Photo.objects.filter(object_id=B.id,content_type__model=M).values(U)[:1];I=D
										if O:I=O[0][U]
										if I:
											F=I.split(V);Z=datetime.now();a=str(K)+'-'+Z.strftime(f);G=F[len(F)-1].split(W)
											if len(G)>1:G=W+G[1]
											else:G=''
											F[len(F)-1]=a+G;L=V.join(F);P=Image.open(os.path.join(R,I));P=P.save(os.path.join(R,L));N=Q
							elif E==_R:
								if Y==0:
									A=getattr(B,E,D)
									if A:
										J=MenuGroup.objects.filter(site_id=K)
										if J:J=J.get()
							else:
								A=getattr(B,E,D)
								if A:setattr(C,E,A)
						C.save()
						if N:Photo.objects.create(content_object=C,file_path=L);
			else:
				B=H.objects.filter(is_initial_data=Q);C=D;N=e
				for S in B:
					C=H();setattr(C,b,K);A=getattr(S,T,D)
					if A:setattr(C,T,A)
					for E in X:
						if E==_E:
							A=getattr(B,E,D)
							if A:
								O=Photo.objects.filter(object_id=B.id,content_type__model=M).values(U)[:1];I=O[0][U]
								if I:
									F=I.split(V);Z=datetime.now();a=str(K)+'-'+Z.strftime(f);G=F[len(F)-1].split(W);
									if len(G)>1:G=W+G[1]
									else:G=''
									F[len(F)-1]=a+G;L=V.join(F);P=Image.open(os.path.join(R,I));P=P.save(os.path.join(R,L));N=Q
						else:
							A=getattr(S,E,D)
							if A:setattr(C,E,A)
				C.save()
				if N:Photo.objects.create(content_object=C,file_path=L);