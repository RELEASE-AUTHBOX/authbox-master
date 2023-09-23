_O='subtitle'
_N='location'
_M='priority'
_L='link'
_K='order_item'
_J=None
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
MODEL_DATA=[{_A:'logo',_B:[_I],_C:[],_D:0},{_A:'favicon',_B:[_I],_C:[],_D:0},{_A:'tags',_B:[_I],_C:[],_D:1},{_A:'categories',_B:[_I],_C:[],_D:1},{_A:'announcement',_B:[_E,_H,_G],_C:[_F,_M],_D:1},{_A:'news',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'article',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'events',_B:[_E,_H,_G,_N],_C:[_F,'date','time'],_D:1},{_A:'slideshow',_B:[_E,_H,_G],_C:[],_D:1},{_A:'dailyalert',_B:['alert'],_C:[_L],_D:1},{_A:'whyus',_B:[_E,_H,'description'],_C:[_F],_D:1},{_A:'greeting',_B:[_E,_G,_I,'designation'],_C:[],_D:1},{_A:'socialmedia',_B:['kind',_L],_C:[],_D:0},{_A:'photogallery',_B:[_E,_G],_C:[_F,_K],_D:1},{_A:'fasilities',_B:[_E,_H,_G],_C:[_F,_K],_D:1},{_A:'offers',_B:[_E,_H,_G],_C:[_F,_K],_D:1},{_A:'howitworks',_B:[_E,_H,_G],_C:['icon',_F,_K],_D:1},{_A:'aboutus',_B:[_E,_H,_G],_C:[_F],_D:1},{_A:'testimony',_B:[_G],_C:[_E,_O,_F],_D:1},{_A:'product',_B:[_I,_E,_H,_G],_C:[_F,_K,'icon','price'],_D:1},{_A:'videogallery',_B:[_E],_C:['embed','embed_video',_F,_K],_D:1},{_A:'relatedlink',_B:[_I],_C:[_L],_D:1},{_A:'document',_B:[_I,_G],_C:[_F],_D:1},{_A:'popup',_B:[_E],_C:[_L],_D:1},{_A:'banner',_B:[_L,_M],_C:[],_D:0},{_A:_N,_B:[_E,_O],_C:['embed',_F],_D:1}]
LANGUAGES=getattr(settings,'LANGUAGES',_J)
def do_init_data(site_id):
	for A in MODEL_DATA:copy_initial_data(site_id,A[_A],A[_B],A[_C],A[_D])
def copy_initial_data(site_id,model,field_trans,field,is_translation):
	P='save complete';O='site_id';L=model;K=True;I=site_id;H='admin_id';D=apps.get_model('frontend',L);print('---------------------');print('proses',L);C=D.objects.filter(site_id=I)
	if not C:
		print('model kosong (lanjutkan)',C);M=D.objects.filter(is_initial_data=K);F=[]
		if M:
			print('data initial data ',M);F=field_trans+field;print('mfield_all',F);J=[];C=D.objects.filter(is_initial_data=K)
			for E in C:J.append(E.id)
			print('m_array',J)
			if is_translation:
				for G in J:
					A=_J
					for (Q,N) in enumerate(LANGUAGES):
						C=D.objects.language(N[0]).get(id=G);print('obj',C)
						if Q==0:A=D();print('obj_create')
						A.set_current_language(N[0]);setattr(A,O,I);B=getattr(C,H,_J)
						if B:setattr(A,H,B)
						for E in F:
							B=getattr(C,E,_J)
							if B:setattr(A,E,B)
						A.save();print(P)
			else:
				print('no translation');C=D.objects.filter(is_initial_data=K);A=_J
				for G in C:
					A=D();setattr(A,O,I);B=getattr(G,H,_J)
					if B:setattr(A,H,B)
					for E in F:
						B=getattr(G,E,_J)
						if B:setattr(A,E,B)
				print('begin save');A.save();print(P)