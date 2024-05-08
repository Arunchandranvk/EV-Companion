from rest_framework import serializers
from ChargingStations.models import ChargingStation

class ChargingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStation
        fields = '__all__'
        
# serializers.py
from rest_framework import serializers
from .models import BookedChargingStation
from UserAccounts.serializers import UserSerializer
from .models import CustomUser 

class BookedChargingStationSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    email = serializers.EmailField(write_only=True)  # Accept email as input
    custom_book_time = serializers.DateTimeField(required=False, allow_null=True)
    price = serializers.SerializerMethodField()
    
    
    class Meta:
        model = BookedChargingStation
        fields = ['id', 'user', 'user_details', 'charging_station', 'booking_time', 'custom_book_time','time', 'email','price']  # Include 'email' field
        extra_kwargs = {
            'user': {'required': False},  # Mark 'user' field as optional
        }

    def create(self, validated_data):
        email = validated_data.pop('email')
        charging_station_id = validated_data.get('charging_station').uid
        user = None
        
        # Check if user exists with the provided email
        if email:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist")

        validated_data['user'] = user
        # Check if charging station exists
        try:
            charging_station = ChargingStation.objects.get(pk=charging_station_id)
        except ChargingStation.DoesNotExist:
            raise serializers.ValidationError("Charging station not found")

        # Check if the price of the charging station matches
        if 'price' in validated_data:
            if validated_data['price'] != charging_station.price:
                raise serializers.ValidationError("Price does not match for the charging station")
        
        return super().create(validated_data)
    def get_price(self, obj):
        return obj.charging_station.price
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('custom_book_time'):
            data.pop('booking_time')
        return data
    
    
    