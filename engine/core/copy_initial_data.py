_O='subtitle'
_N='location'
_M='priority'
_L='link'
_K='order_item'
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
from datetime import datetime
from django.apps import apps
from django.conf import settings
from core.models import Photo
from PIL import Image
MODEL_DATA=[{_A:'logo',_B:[_J],_C:[_E],_D:0},{_A:'favicon',_B:[_J],_C:[_E],_D:0},{_A:'tags',_B:[_J],_C:[],_D:1},{_A:'categories',_B:[_J],_C:[],_D:1},{_A:'announcement',_B:[_F,_I,_H],_C:[_G,_M,_E],_D:1},{_A:'news',_B:[_F,_I,_H],_C:[_G,_E],_D:1},{_A:'article',_B:[_F,_I,_H],_C:[_G,_E],_D:1},{_A:'events',_B:[_F,_I,_H,_N],_C:[_G,'date','time',_E],_D:1},{_A:'slideshow',_B:[_F,_I,_H],_C:[_E],_D:1},{_A:'dailyalert',_B:['alert'],_C:[_L],_D:1},{_A:'whyus',_B:[_F,_I,'description'],_C:[_G],_D:1},{_A:'greeting',_B:[_F,_H,_J,'designation'],_C:[_E],_D:1},{_A:'socialmedia',_B:['kind',_L],_C:[],_D:0},{_A:'photogallery',_B:[_F,_H],_C:[_G,_K,_E],_D:1},{_A:'fasilities',_B:[_F,_I,_H],_C:[_G,_K,_E],_D:1},{_A:'offers',_B:[_F,_I,_H],_C:[_G,_K,_E],_D:1},{_A:'howitworks',_B:[_F,_I,_H],_C:['icon',_G,_K,_E],_D:1},{_A:'aboutus',_B:[_F,_I,_H],_C:[_G,_E],_D:1},{_A:'testimony',_B:[_H],_C:[_F,_O,_G,_E],_D:1},{_A:'product',_B:[_J,_F,_I,_H],_C:[_G,_K,'icon','price',_E],_D:1},{_A:'videogallery',_B:[_F],_C:['embed','embed_video',_G,_K,_E],_D:1},{_A:'relatedlink',_B:[_J],_C:[_L],_D:1},{_A:'document',_B:[_J,_H],_C:[_G,_E],_D:1},{_A:'popup',_B:[_F],_C:[_L,_E],_D:1},{_A:'banner',_B:[_L,_M],_C:[_E],_D:0},{_A:_N,_B:[_F,_O],_C:['embed',_G],_D:1}]
@transaction.atomic
def do_init_data(site_id):
	for A in MODEL_DATA:copy_initial_data(site_id,A[_A],A[_B],A[_C],A[_D])
def copy_initial_data(site_id,model,field_trans,field,is_translation):
	Z='save complete';Y='file_path';X='site_id';Q=model;P='admin_id';O=True;I=site_id;D=None;a=getattr(settings,'LANGUAGES',D);R=getattr(settings,'MEDIA_ROOT',D);F=apps.get_model('frontend',Q);print('---------------------');print('proses',Q);C=F.objects.filter(site_id=I)
	if not C:
		print('model kosong (lanjutkan)',C);T=F.objects.filter(is_initial_data=O);J=[]
		if T:
			print('data initial data ',T);J=field_trans+field;print('mfield_all',J);S=[];C=F.objects.filter(is_initial_data=O)
			for E in C:S.append(E.id)
			print('m_array',S)
			if is_translation:
				for K in S:
					A=D
					for (U,V) in enumerate(a):
						C=F.objects.language(V[0]).get(id=K)
						if U==0:A=F();print('obj_create')
						A.set_current_language(V[0]);setattr(A,X,I);B=getattr(C,P,D)
						if B:setattr(A,P,B)
						W=False;L=D
						for E in J:
							if E==_E:
								if U==0:
									W=O;print('proses photo');B=getattr(C,E,D)
									if B:
										b=Photo.objects.filter(object_id=C.id,content_type__model=Q).values(Y)[:1];M=b[0][Y];G=M.split('/');print('file_name',G);c=datetime.now();d=str(I)+'-'+c.strftime('%Y%m%d-%H%M%S-%f');H=G[len(G)-1].split('.');print('extension',H)
										if len(H)>1:H='.'+H[1]
										else:H=''
										G[len(G)-1]=d+H;L='/'.join(G);print('new_url',L);print('url',M);print('path',os.path.join(R,M));N=Image.open(os.path.join(R,M));print('im',N);N=N.save(os.path.join(R,L));print('im.save',N)
							else:
								B=getattr(C,E,D)
								if B:setattr(A,E,B)
						A.save()
						if W:Photo.objects.create(content_object=A,file_path=L);print('save photo complete')
						print(Z)
			else:
				print('no translation');C=F.objects.filter(is_initial_data=O);A=D
				for K in C:
					A=F();setattr(A,X,I);B=getattr(K,P,D)
					if B:setattr(A,P,B)
					for E in J:
						B=getattr(K,E,D)
						if B:setattr(A,E,B)
				print('begin save');A.save();print(Z)