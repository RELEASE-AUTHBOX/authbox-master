from django_authbox.common import get_natural_datetime
import datetime
from django import template
register=template.Library()
@register.filter
def phone_number(number):
	B='-';A=number
	if A:
		G=['62','60','65','63','66','84']
		if A[:2]in G:C=A[:2];D=A[2:4];E=A[4:7];F=A[7:10];H=A[10:];return'('+C+')'+' '+D+B+E+B+F+B+H
		elif A:C=A[:3];D=A[3:6];E=A[6:9];F=A[9:];return'('+C+')'+' '+D+B+E+B+F
	return''
@register.filter
def replace_with(string,find_replace=',|_'):A,B=find_replace.split('|');return string.replace(A,B)
@register.filter
def natural_datetime(data_datetime):A=datetime.datetime.now();return get_natural_datetime(data_datetime,A)
@register.filter
def get_class(value):return value[0].__class__.__name__.lower()