from django.db import models

# Create your models here.
class TurfDb(models.Model):
    turf_name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    turf_type=models.CharField(max_length=100,default="Football")
    price_per_hour=models.PositiveIntegerField()
    opening_time=models.TimeField()
    closing_time=models.TimeField()
    is_available=models.BooleanField(default=True)


    def __str__(self):
        return self.turf_name

class BookingDb(models.Model):
    turf=models.ForeignKey(TurfDb,on_delete=models.CASCADE)
    customer_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    booking_date=models.DateField()
    duration = models.PositiveIntegerField(default=1)
    booking_time=models.TimeField()
    amount=models.IntegerField()
    status=models.CharField(max_length=100,default="pending")


    def __str__(self):
        return self.customer_name