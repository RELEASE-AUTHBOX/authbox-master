_O='subtitle'
_N='location'
_M='priority'
_L='link'
_K=None
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
MODEL_DATA=[{_A:'logo',_B:[_I],_C:[],_D:0},{_A:'favicon',_B:[_I],_C:[],_D:0},{_A:'tags',_B:[_I],_C:[],_D:1},{_A:'categories',_B:[_I],_C:[],_D:1},{_A:'announcement',_B:[_E,_H,_G],_C:[_F,_M],_D:1},{_A:'news',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'article',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'events',_B:[_E,_H,_G,_N],_C:[_F,'date','time'],_D:1},{_A:'slideshow',_B:[_E,_H,_G],_C:[],_D:1},{_A:'dailyalert',_B:['alert'],_C:[_L],_D:1},{_A:'whyus',_B:[_E,_H,'description'],_C:[_F],_D:1},{_A:'greeting',_B:[_E,_G,_I,'designation'],_C:[],_D:1},{_A:'socialmedia',_B:['kind',_L],_C:[],_D:0},{_A:'photogallery',_B:[_E,_G],_C:[_F,_J],_D:1},{_A:'fasilities',_B:[_E,_H,_G],_C:[_F,_J],_D:1},{_A:'offers',_B:[_E,_H,_G],_C:[_F,_J],_D:1},{_A:'howitworks',_B:[_E,_H,_G],_C:['icon',_F,_J],_D:1},{_A:'aboutus',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'testimony',_B:[_G],_C:[_E,_O,_F],_D:1},{_A:'product',_B:[_I,_E,_H,_G],_C:[_F,_J,'icon','price'],_D:1},{_A:'videogallery',_B:[_E],_C:['embed','embed_video',_F,_J],_D:1},{_A:'relatedlink',_B:[_I],_C:[_L],_D:1},{_A:'document',_B:[_I,_G],_C:[_F],_D:1},{_A:'popup',_B:[_E],_C:[_L],_D:1},{_A:'banner',_B:[_L,_M],_C:[],_D:0},{_A:_N,_B:[_E,_O],_C:['embed',_F],_D:1}]
LANGUAGES=getattr(settings,'LANGUAGES',_K)
def do_init_data(site_id):
	for A in MODEL_DATA:copy_initial_data(site_id,A[_A],A[_B],A[_C],A[_D])
def copy_initial_data(site_id,model,field_trans,field,is_translation):
	Q='save complete';P='begin save';O='site_id';L=model;K=True;I=site_id;H='admin_id';D=apps.get_model('frontend',L);print('---------------------');print('proses',L);C=D.objects.filter(site_id=I)
	if not C:
		print('model kosong (lanjutkan)',C);M=D.objects.filter(is_initial_data=K);G=[]
		if M:
			print('data initial data ',M);G=field_trans+field;print('mfield_all',G);A=_K;N=0
			if is_translation:
				for J in LANGUAGES:
					print('lang',J[0]);C=D.objects.language(J[0]).filter(is_initial_data=K)
					if N==0:A=D();N+=1
					A.set_current_language(J[0]);setattr(A,O,I)
					for E in C:
						B=getattr(E,H,_K)
						if B:setattr(A,H,B)
						for F in G:
							B=getattr(E,F,_K)
							if B:setattr(A,F,B)
					print(P);A.save();print(Q)
			else:
				print('no translation');C=D.objects.filter(is_initial_data=K);print('obj',C);A=D();setattr(A,O,I)
				for E in C:
					B=getattr(E,H,_K)
					if B:setattr(A,H,B)
					for F in G:
						B=getattr(E,F,_K)
						if B:setattr(A,F,B)
				print(P);A.save();print(Q)