from rest_framework import serializers
from dmirs.models import DataFileColumn


class DataFileColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFileColumn
        fields = '__all__'
