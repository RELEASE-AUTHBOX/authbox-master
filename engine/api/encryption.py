import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from django.conf import settings
from.base62 import base62_encode,base62_decode
AES_KEY=getattr(settings,'AES_KEY',None)
if not AES_KEY:raise ValueError('AES_KEY is not set in settings.py')
if isinstance(AES_KEY,str):import binascii;AES_KEY=binascii.unhexlify(AES_KEY)
aesgcm=AESGCM(AES_KEY)
def encrypt_data(data):A=os.urandom(12);B=aesgcm.encrypt(A,data.encode(),None);return base62_encode(A+B)
def decrypt_data(token):
	try:A=base62_decode(token);B,C=A[:12],A[12:];D=aesgcm.decrypt(B,C,None).decode();return D
	except Exception:raise ValueError('Invalid or tampered data token')