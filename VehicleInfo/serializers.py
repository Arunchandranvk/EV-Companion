from rest_framework import serializers
from VehicleInfo.models import Vehicles

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'