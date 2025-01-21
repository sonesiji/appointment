from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.utils.timezone import now
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Models
from django.db import models
from django.utils.timezone import now

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='instructors/')
    rpc_number = models.CharField(max_length=50)
    experience = models.TextField()
    issued_date = models.DateField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class BookingSlot(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["date", "time"], name="unique_slot_per_datetime")
        ]

    def save(self, *args, **kwargs):
        # Ensure the admin cannot create duplicate slots for the same date and time
        if BookingSlot.objects.filter(date=self.date, time=self.time).exists() and not self.pk:
            raise ValidationError("A slot with this date and time already exists.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {self.time} ({'Booked' if self.is_booked else 'Available'})"



class UserBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    drone_details = models.TextField()
    slot = models.OneToOneField(BookingSlot, on_delete=models.CASCADE)
    slot_date = models.DateField(editable=False)  # New field to store slot date
    created_at = models.DateTimeField(default=now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email", "phone_number", "slot_date"],
                name="unique_booking_per_day_per_user",
            )
        ]

    def save(self, *args, **kwargs):
        if self.slot.is_booked:
            raise ValidationError("This slot is already booked.")
        super().save(*args, **kwargs)
        # Mark the slot as booked after saving
        self.slot.is_booked = True
        self.slot.save()

    def __str__(self):
        return f"Booking for {self.name} on {self.slot.date} {self.slot.time}"
