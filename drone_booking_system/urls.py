# from django.contrib import admin
# from django.urls import path
# from myapp import views
# from myapp.views import (
#     instructor_details,
#     slot_booking,
#     payment_page,
#     view_bookings,
# )
# from django.contrib.auth.views import LoginView
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', instructor_details, name='instructor_details'),
#     path('book/', slot_booking, name='slot_booking'),
#     path('payment/', payment_page, name='payment'),
#     path('view-bookings/', view_bookings, name='view_bookings'),
#     path('login/', LoginView.as_view(template_name='login.html'), name='login'),
#     path('available-times/', views.available_times, name='available_times'),
# ]

# # Serve static and media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from django.contrib import admin
# from django.urls import path
# from myapp import views
# from myapp.views import (
#     instructor_details,
#     slot_booking,
#     payment_page,
#     view_bookings,
#     confirm_payment,  # Added to handle payment confirmation
# )
# from django.contrib.auth.views import LoginView
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', instructor_details, name='instructor_details'),  # Homepage with instructor details
#     path('book/', slot_booking, name='slot_booking'),  # Slot booking page
#     path('payment/', payment_page, name='payment'),  # Dummy payment page
#     path('confirm-payment/', confirm_payment, name='confirm_payment'),  # Confirm payment and finalize booking
#     path('view-bookings/', view_bookings, name='view_bookings'),  # View user bookings
#     path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Login page
#     path('available-times/', views.available_times, name='available_times'),  # Get available time slots
# ]

# # Serve static and media files in development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import (
    instructor_details,
    slot_booking,
    payment_page,
    view_bookings,
    confirm_payment,  # Handle confirmation of payment
)
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', instructor_details, name='instructor_details'),  # Instructor details page
    path('book/', slot_booking, name='slot_booking'),  # Slot booking page
    path('payment/<int:booking_id>/', payment_page, name='payment'),  # Redirects to payment page with booking_id
    
    # path('confirm-payment/<int:booking_id>/', confirm_payment, name='confirm_payment'),  # Finalize booking after payment
    path('confirm-payment/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),
   

    path('view-bookings/', view_bookings, name='view_bookings'),  # View user bookings page
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Login page
    path('available-times/', views.available_times, name='available_times'),  # Get available times
    
      path('slot-booking/', views.slot_booking, name='slot_booking'),
    path('get-booked-slots/', views.get_booked_slots, name='get_booked_slots'),

    path('view-bookings/', views.view_bookings, name='view_bookings'),





    
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
