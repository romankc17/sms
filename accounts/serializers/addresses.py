from rest_framework import serializers

from ..models.addresses import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'village',
            'ward_no',
            'tole'
        )