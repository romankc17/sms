from rest_framework import serializers

from .models import Class, Batch, Section

class ClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    class Meta:
        model = Class
        fields = ('id', 'name')

class BatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(required=True)
    classes = ClassSerializer(many=True)

    class Meta:
        model = Batch
        fields = ('id', 'year', 'classes')

class SectionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Section
        fields = ('id', 'name')


