from rest_framework import serializers

from ..models.students import Student
from ..models.addresses import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('village', 'ward_no', 'tole')

class StudentSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Student
        fields = (
            'id',
            'name',
            'roll_no',
            'dob',
            'parent_name',
            'parent_contact',
            'image',
            'gender'
        )

    # customizing create to create student with address
    def create(self, validated_data):
        # Populating address data
        address_data = validated_data.pop('address')

        # creating a student
        student = Student(**validated_data)
        student.save()

        # creating address
        Address.objects.create(student=student, **address_data)
        return student

    # customizing update to update student with address
    def update(self, instance, validated_data):
        # Check if the address is in update data
        address_data = validated_data.get('address')

        # Update address if in update data
        if address_data:
            address_data = validated_data.pop('address')
            address_instance = instance.address
            for attr, value in address_data.items():
                setattr(address_instance, attr, value)
            address_instance.save()
        

        # updating student
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        