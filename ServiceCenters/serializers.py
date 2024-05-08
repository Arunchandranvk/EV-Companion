# serializers.py
from rest_framework import serializers
from .models import ServiceCenter,  DeliveryBoy,ServiceCenterBooking

# class ServiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Service
#         fields = ['id', 'name', 'price']


class ServiceCenterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServiceCenter
        fields = '__all__'

class DeliveryBoySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryBoy
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'address']
        
        
# serializers.py
from rest_framework import serializers
from .models import AssignedDelivery,CustomUser

class AssignedDeliverySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    deliveryboy_name = serializers.CharField(source='delivery_boy.first_name')

    class Meta:
        model = AssignedDelivery
        fields = ['id', 'username', 'deliveryboy_name', 'destination_address', 'delivery_status', 'phone_number']
        extra_kwargs = {
            'delivery_status': {'required': False}, 
        }

    def create(self, validated_data):
        # Extract the username and delivery boy name from validated_data
        username = validated_data.pop('user')['username']
        deliveryboy_name = validated_data.pop('delivery_boy')['first_name']
        
        # Get the user and delivery boy instances
        user_instance = CustomUser.objects.get(username=username)
        delivery_boy_instance = DeliveryBoy.objects.get(first_name=deliveryboy_name)
        
        # Create the AssignedDelivery instance
        assigned_delivery_instance = AssignedDelivery.objects.create(
            user=user_instance,
            delivery_boy=delivery_boy_instance,
            **validated_data
        )
        return assigned_delivery_instance





class ServiceCenterBookingSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    charging_station_name = serializers.CharField(source='service_center.name')

    class Meta:
        model = ServiceCenterBooking
        fields = ['email', 'charging_station_name', 'booking_time', 'custom_book_time', 'time','need_delivery_boy']
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('custom_book_time'):
            data.pop('booking_time')
        return data

    def create(self, validated_data):
        # Extract the username and charging_station_name from validated_data
        email = validated_data.pop('user')['email']
        charging_station_name = validated_data.pop('service_center')['name']
        
        # Get the user and service center instances
        user_instance = CustomUser.objects.get(email=email)
        service_center_instance = ServiceCenter.objects.get(name=charging_station_name)
        
        # Create the ServiceCenterBooking instance
        booking_instance = ServiceCenterBooking.objects.create(
            user=user_instance,
            service_center=service_center_instance,
            **validated_data
        )
        return booking_instance

    