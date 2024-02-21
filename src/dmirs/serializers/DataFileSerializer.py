from rest_framework import serializers
from dmirs.models import DataFile

from .DataFileHeaderSerializer import DataFileHeaderSerializer
from .DataFileColumnSerializer import DataFileColumnSerializer


class DataFileSerializer(serializers.ModelSerializer):
    headers = DataFileHeaderSerializer(many=True, read_only=True)
    columns = DataFileColumnSerializer(many=True, read_only=True)

    class Meta:
        model = DataFile
        fields = '__all__'
