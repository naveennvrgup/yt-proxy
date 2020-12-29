from rest_framework import serializers
from .models import YTVideo


# helps to serialise output
class YTVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=YTVideo
        fields = '__all__' # all the fields of the model is used