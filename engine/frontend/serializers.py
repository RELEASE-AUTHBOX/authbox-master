from.models import DirectUpdate
from rest_framework import serializers
from django.db.models import ImageField
class DirectUpdateSerializer(serializers.ModelSerializer):
	value_image_url=serializers.SerializerMethodField()
	class Meta:model=DirectUpdate;fields=['id','site','code','value_type','value_text','value_textarea','value_image_url']
	def get_value_image_url(C,obj):
		A=obj.value_image.first()
		if A and A.file_path:
			B=C.context.get('request')
			if B:return B.build_absolute_uri(A.file_path.url)
			return A.file_path.url