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

    def __str__(self):
        return f"{self.date} {self.time} ({'Booked' if self.is_booked else 'Available'})"

class UserBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    drone_details = models.TextField()
    slot = models.OneToOneField(BookingSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Booking for {self.name} on {self.slot.date} {self.slot.time}"