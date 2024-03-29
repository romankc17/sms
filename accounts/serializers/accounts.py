from rest_framework import serializers

from accounts.models import Account

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self,attr):
        data = super().validate(attr)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        return data
    
    


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # setting is_active true by default
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = Account
        fields = (
            'id', 
            'username',
            'email', 
            'password', 
            'is_staff', 
            'is_active', 
            'is_admin',
            'is_superuser',
            'date_joined'
        )
        extra_kwargs = {'password': {'write_only': True}}

    # check if the email already exist

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    # customizing update method for account
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
        


