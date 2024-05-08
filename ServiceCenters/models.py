from django.db import models
from UserAccounts.models import CustomUser

class ServiceCenter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    services_offered = models.CharField(max_length=200,null=True)
    need_delivery_boy = models.BooleanField(default=False)
    price=models.DecimalField(max_digits=9, decimal_places=6, default=0)

    def __str__(self):
        return self.name
    

class DeliveryBoy(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=200)

    def _str_(self):
        return f"{self.first_name} {self.last_name}"
    
class AssignedDelivery(models.Model):
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    destination_address = models.CharField(max_length=200)
    delivery_status = models.CharField(max_length=50)
    phone_number=models.CharField(max_length=20,null=True)

    def __str__(self):
        return f"Delivery by {self.delivery_boy} to {self.destination_address}"
    
class ServiceCenterBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_center = models.ForeignKey(ServiceCenter, on_delete=models.CASCADE, null=True)
    booking_time = models.DateTimeField(auto_now_add=True)
    custom_book_time = models.DateTimeField(null=True)
    price=models.DecimalField(max_digits=9, decimal_places=6, default=0)
    time=models.TimeField(null=True)
    need_delivery_boy = models.BooleanField(default=False,null=True)

    def __str__(self):
        return f"Booking ID: {self.id} - User: {self.user.username} - Service Center: {self.service_center.name}"