_N='subtitle'
_M='location'
_L='priority'
_K='link'
_J='order_item'
_I='name'
_H='sub_title'
_G='content'
_F='is_header_text'
_E='title'
_D='is_translation'
_C='field'
_B='field_trans'
_A='model'
from django.apps import apps
from django.conf import settings
MODEL_DATA=[{_A:'logo',_B:[_I],_C:[],_D:0},{_A:'favicon',_B:[_I],_C:[],_D:0},{_A:'tags',_B:[_I],_C:[],_D:1},{_A:'categories',_B:[_I],_C:[],_D:1},{_A:'announcement',_B:[_E,_H,_G],_C:[_F,_L],_D:1},{_A:'news',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'article',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'events',_B:[_E,_H,_G,_M],_C:[_F,'date','time'],_D:1},{_A:'slideshow',_B:[_E,_H,_G],_C:[],_D:1},{_A:'dailyalert',_B:['alert'],_C:[_K],_D:1},{_A:'whyus',_B:[_E,_H,'description'],_C:[_F],_D:1},{_A:'greeting',_B:[_E,_G,_I,'designation'],_C:[],_D:1},{_A:'socialmedia',_B:['kind',_K],_C:[],_D:0},{_A:'photogallery',_B:[_E,_G],_C:[_F,_J],_D:1},{_A:'fasilities',_B:[_E,_H,_G],_C:[_F,_J],_D:1},{_A:'offers',_B:[_E,_H,_G],_C:[_F,_J],_D:1},{_A:'howitworks',_B:[_E,_H,_G],_C:['icon',_F,_J],_D:1},{_A:'aboutus',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'testimony',_B:[_G],_C:[_E,_N,_F],_D:1},{_A:'product',_B:[_I,_E,_H,_G],_C:[_F,_J,'icon','price'],_D:1},{_A:'videogallery',_B:[_E],_C:['embed','embed_video',_F,_J],_D:1},{_A:'relatedlink',_B:[_I],_C:[_K],_D:1},{_A:'document',_B:[_I,_G],_C:[_F],_D:1},{_A:'popup',_B:[_E],_C:[_K],_D:1},{_A:'banner',_B:[_K,_L],_C:[],_D:0},{_A:_M,_B:[_E,_N],_C:['embed',_F],_D:1}]
LANGUAGES=getattr(settings,'LANGUAGES',None)
def do_init_data(site_id):
	for A in MODEL_DATA:copy_initial_data(site_id,A[_A],A[_B],A[_C],A[_D])
def copy_initial_data(site_id,model,field_trans,field,is_translation):
	Q='save complete';P='begin save';O='admin_id';N='site_id';M='obj';J=model;I=True;F=site_id;C=apps.get_model('frontend',J);print('---------------------');print('proses',J);B=C.objects.filter(site_id=F)
	if not B:
		print('model kosong (lanjutkan)',B);K=C.objects.filter(is_initial_data=I);E=[]
		if K:
			print('data initial data ',K);E=field_trans+field;print('mfield_all',E);A=None;L=0
			if is_translation:
				for G in LANGUAGES:
					print('lang',G[0]);B=C.objects.language(G[0]).filter(is_initial_data=I);print(M,B)
					if L==0:A=C();L+=1
					print('obj_create',A);A.set_current_language(G[0]);setattr(A,N,F);setattr(A,O,'1')
					for H in B:
						for D in E:setattr(A,D,getattr(H,D))
					print(P);A.save();print(Q)
			else:
				print('no translation');B=C.objects.filter(is_initial_data=I);print(M,B);A=C();setattr(A,N,F);setattr(A,O,'1')
				for H in B:
					for D in E:setattr(A,D,getattr(H,D))
				print(P);A.save();print(Q)