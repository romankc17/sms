from rest_framework import serializers

from .models import Exam, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            'id', 
            'name', 
            'pass_mark', 
            'full_mark'
        )


class ExamSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Exam
        fields = (
            'id', 
            'name', 
            'date',
            'subjects'
        )

    # customize create exam
    def create(self, validated_data):
        subjects = validated_data.pop('subjects')
        exam = Exam.objects.create(**validated_data)
        for subject in subjects:
            Subject.objects.create(exam=exam, **subject)
        return exam

    # customize update exam
    def update(self, instance, validated_data):
        subjects = validated_data.pop('subjects')
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        for subject in subjects:
            Subject.objects.update_or_create(exam=instance, **subject)
        return instance