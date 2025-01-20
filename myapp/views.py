from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Instructor, BookingSlot, UserBooking

@login_required
def instructor_details(request):
    instructor = Instructor.objects.first()
    return render(request, 'instructor_details.html', {'instructor': instructor})

def slot_booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        drone_details = request.POST['drone_details']
        date = request.POST['date']
        time = request.POST['time']

        # Find the specific slot
        slot = BookingSlot.objects.filter(date=date, time=time, is_booked=False).first()
        if not slot:
            return HttpResponse('The selected slot is already booked or unavailable.')

        # Create booking and mark slot as booked
        booking = UserBooking.objects.create(
            name=name, email=email, address=address,
            phone_number=phone_number, drone_details=drone_details, slot=slot
        )
        slot.is_booked = True
        slot.save()

        send_mail(
            'Booking Confirmation',
            f'Thank you for booking! Your slot on {slot.date} at {slot.time} is confirmed.',
            'noreply@example.com',
            [email]
        )
        # return redirect('payment_page')
        return redirect('payment', booking_id=booking.id)


    slots = BookingSlot.objects.filter(is_booked=False)
    return render(request, 'slot_booking.html', {'slots': slots})

def payment_page(request):
    return HttpResponse('<h1>Dummy Payment Page</h1><a href="/">Back to Home</a>')

@login_required
def view_bookings(request):
    bookings = UserBooking.objects.select_related('slot').all()
    return render(request, 'view_bookings.html', {'bookings': bookings})



from django.http import JsonResponse
from .models import BookingSlot

def available_times(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'Date is required'}, status=400)

    # Get available times for the selected date
    slots = BookingSlot.objects.filter(date=date, is_booked=False).values_list('time', flat=True)
    times = [slot.strftime('%H:%M') for slot in slots]  # Format time as HH:MM

    return JsonResponse({'times': times})


def confirm_payment(request):
    # Your function logic here
    pass
