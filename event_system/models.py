from django.db import models
from django.core.exceptions import ValidationError

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    seating_capacity = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity, related_name='halls')
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class HallImage(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hall_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hall.name}"


from django.core.exceptions import ValidationError

# class Booking(models.Model):
#     hall = models.ForeignKey('Hall', on_delete=models.CASCADE, related_name='bookings')
#     customer_name = models.CharField(max_length=255)
#     customer_email = models.EmailField()
#     start_datetime = models.DateTimeField(null=True, blank=True)
#     end_datetime = models.DateTimeField(null=True, blank=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

#     def clean(self):
#         if self.start_datetime and self.end_datetime:
#             if self.start_datetime >= self.end_datetime:
#                 raise ValidationError("End datetime must be after start datetime.")

#     def save(self, *args, **kwargs):
#         self.clean()

#         if not self.start_datetime or not self.end_datetime:
#             raise ValueError("Start and end datetime must be set before saving.")

#         duration = self.end_datetime - self.start_datetime
#         days = duration.days
#         if duration.seconds > 0:
#             days += 1
#         if days <= 0:
#             days = 1

#         self.total_price = days * self.hall.price_per_day
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Booking for {self.hall.name} by {self.customer_name}"
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    hall = models.ForeignKey('Hall', on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # <- New field

    def clean(self):
        if self.start_datetime and self.end_datetime:
            if self.start_datetime >= self.end_datetime:
                raise ValidationError("End datetime must be after start datetime.")

    def save(self, *args, **kwargs):
        self.clean()

        if not self.start_datetime or not self.end_datetime:
            raise ValueError("Start and end datetime must be set before saving.")

        duration = self.end_datetime - self.start_datetime
        days = duration.days
        if duration.seconds > 0:
            days += 1
        if days <= 0:
            days = 1

        self.total_price = days * self.hall.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.hall.name} by {self.customer_name}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES,default='upi_id')
    
    # Optional fields, depending on payment method
    card_number = models.CharField(max_length=16, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.payment_method} - ₹{self.amount} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

