from os import read
from rest_framework import serializers
from rest_framework.response import Response


from .models import Class, Batch, Section

class SectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Section
        fields = ('id','name',)

# Serilizer for Class model along with Section
class ClassSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    sections = SectionSerializer(many=True)

    class Meta:
        model = Class
        fields = ('id','name', 'sections')

    def create(self, validated_data):
        sections_data = validated_data.pop('sections')
        class_ = Class.objects.create(**validated_data)
        for section_data in sections_data:
            Section.objects.create(class_name=class_, **section_data)
        return class_

    def update(self, instance, validated_data):
        sections_data = validated_data.pop('sections')
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        for section_data in sections_data:

            # create new section if section id is not PROVIDED
            if not section_data.get('id'):

                # check if the section name already exists in the same class
                if Section.objects.filter(name=section_data.get('name'), class_name=instance).exists():
                    # raise serializers.ValidationError('Section already exists')
                    return Response(
                        {
                            "status":"eroor",
                            "message":"Section already exists",
                            "data":{
                                "name": ["Section name already exists"]
                            }
                        },
                        status=400
                    )

                Section.objects.create(class_name=instance, **section_data)
                
            else:
                # update existing section
                section = Section.objects.get(id=section_data['id'])
                section.name = section_data.get('name', section.name)
                section.save()
        return instance

class BatchSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True, write_only=True)

    class Meta:
        model = Batch
        fields = (
            'year',
            'classes'
        )
    

    # Creating batch, classes and sections with nested serializers
    def create(self, validated_data):
        classes_data = validated_data.pop('classes')
        batch = Batch.objects.create(**validated_data)

        for class_data in classes_data:
            class_serializer = ClassSerializer(data=class_data)
            if class_serializer.is_valid():
                # Creating new class object with batch 
                class_serializer.save(batch=batch)
        return batch


    # Updating batch, classes and sections with nested serializers
    def update(self, instance, validated_data):
        
        classes_data = validated_data.pop('classes')
        instance.year = validated_data.get('year', instance.year)
        instance.save()

        for class_data in classes_data:
            class_id = class_data.get('id')
            class_qs = Class.objects.filter(id=class_id, batch=instance)

            # create new class if class id is not provided or class does not exist
            if class_id is None or not class_qs.exists():

                # Create new class object with batch
                class_serializer = ClassSerializer(data=class_data)
                if class_serializer.is_valid():
                    class_serializer.save(batch=instance)

            else:
                # update existing class
                class_ = class_qs.first()
                class_serializer = ClassSerializer(class_, data=class_data)
                if class_serializer.is_valid():
                    class_serializer.save(batch=instance)
        return instance
        




