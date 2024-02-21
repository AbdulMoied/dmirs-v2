from rest_framework import serializers
from dmirs.models import DataFileHeader
from .MetaHeaderSerializer import MetaHeaderSerializer


class DataFileHeaderSerializer(serializers.ModelSerializer):
    header = MetaHeaderSerializer()

    class Meta:
        model = DataFileHeader
        fields = '__all__'
