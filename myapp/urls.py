
from django.contrib import admin
from django.urls import path
from .views import instructor_details, slot_booking, payment_page, view_bookings
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', instructor_details, name='instructor_details'),
    path('book/', slot_booking, name='slot_booking'),
    path('payment/', payment_page, name='payment'),
    path('view-bookings/', view_bookings, name='view_bookings'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]