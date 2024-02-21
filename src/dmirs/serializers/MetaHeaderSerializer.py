from rest_framework import serializers

from dmirs.models import MetaHeader


class MetaHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaHeader
        fields = '__all__'
