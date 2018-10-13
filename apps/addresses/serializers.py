from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "street_1",
            "street_2",
            "zip_code",
            "city",
            "country",
            "primary",
        )
