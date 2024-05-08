from django.db import models
import uuid


class Vehicles(models.Model):
    uid=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    make=models.CharField(max_length=100)
    model=models.CharField(max_length=100)
    year=models.PositiveBigIntegerField()
    battery_capacity=models.DecimalField(max_digits=5, decimal_places=2)
    charging_time=models.PositiveBigIntegerField()
    vehicle_image=models.ImageField(upload_to="vehicles")

    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model}"