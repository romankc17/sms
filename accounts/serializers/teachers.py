from rest_framework import serializers

from ..models.teachers import Teacher

from ..serializers.accounts import AccountSerializer

# Serializer for Teacher model
class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(required=False,max_length=None,allow_empty_file=True,use_url=True)

    class Meta:
        model = Teacher
        fields = (
            'id',
            'email',
            'name',
            'village',
            'ward_no',
            'tole',
            'phone',
            'joining_date',
            'role',
            'image',
            'gender'
        )

