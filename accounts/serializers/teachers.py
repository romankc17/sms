from rest_framework import serializers

from ..models.teachers import Teacher
from ..models.addresses import Address

from ..serializers.accounts import AccountSerializer
from ..serializers.addresses import AddressSerializer

# Serializer for Teacher model
class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    address = AddressSerializer(required=False)
    salary = serializers.IntegerField(required=False)
    username = serializers.CharField(source='account.username')
    email = serializers.CharField(source='account.email')
    password = serializers.CharField(write_only=True, source='account.password')

    class Meta:
        model = Teacher
        fields = (
            'id',
            'username',
            'email',
            'password',
            'name',
            'address',
            'phone',
            'salary',
            'joining_date',
            'role',
            'image',
            'gender'
        )

    def create(self, validated_data):
        # creating a account
        account_data = validated_data.pop('account')
        account_data['is_staff'] = True
        account_data['is_admin'] = False
        account_data['is_superuser'] = False
        account_data['is_active'] = True

        # Using AccountSerializer to create account
        account_serializer = AccountSerializer(data=account_data)
        account_serializer.is_valid(raise_exception=True)
        account = account_serializer.save()

        # Populating address data
        address_data = validated_data.pop('address')

        # creating a teacher
        teacher = Teacher(**validated_data)
        teacher.account = account
        teacher.save()

        # creating address
        Address.objects.create(teacher=teacher, **address_data)
        return teacher

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
        
        # Check if the account is in update data
        account_data = validated_data.get('account')
        # Update account if in update data
        if account_data:
            account_data = validated_data.pop('account')
            account_instance = instance.account
            
            account_serializer = AccountSerializer(account_instance, data=account_data, partial=True)
            
            account_serializer.is_valid(raise_exception=True)
            account_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
