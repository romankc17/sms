from rest_framework import serializers

from accounts.models import Account


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
            'name', 
            'is_staff', 
            'is_active', 
            'is_admin',
            'is_superuser',
            'date_joined'
        )
        extra_kwargs = {'password': {'write_only': True}}

    # customizing create method for account 
    #  
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance
    
        


