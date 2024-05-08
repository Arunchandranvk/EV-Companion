from django.db import models
import uuid
from UserAccounts.models import CustomUser
# Create your models here.
class ChargingStation(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Example precision for latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Example precision for longitude
    address = models.CharField(max_length=200)
    operating_hours = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='charging_station_images/', null=True, blank=True)
    contact_info = models.CharField(max_length=100)
    operational_status = models.BooleanField(default=True)
    price=models.DecimalField(max_digits=9, decimal_places=6, default=0)
    booked_status=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class BookedChargingStation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)#email
    charging_station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)#station name
    booking_time = models.DateTimeField(auto_now_add=True)
    custom_book_time=models.DateTimeField(null=True)
    time=models.TimeField(null=True)
    price = models.DecimalField(max_digits=9, decimal_places=6, default=0,null=True)
    # Add more fields as needed, such as charging duration, payment status, etc.

    def __str__(self):
        return f"Booking for {self.user} at {self.charging_station}"

    


    
