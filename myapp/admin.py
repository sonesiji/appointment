from django.contrib import admin
from django.contrib import admin
from .models import Instructor, BookingSlot, UserBooking

# Register your models here.
admin.site.register(Instructor)
admin.site.register(BookingSlot)
admin.site.register(UserBooking)
