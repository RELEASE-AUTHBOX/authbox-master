BASE62_ALPHABET='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def base62_encode(data):
	A=int.from_bytes(data,'big')
	if A==0:return BASE62_ALPHABET[0]
	B=[]
	while A>0:A,C=divmod(A,62);B.append(BASE62_ALPHABET[C])
	return''.join(reversed(B))
def base62_decode(s):
	A=0
	for B in s:A=A*62+BASE62_ALPHABET.index(B)
	C=(A.bit_length()+7)//8;return A.to_bytes(C,'big')