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

# def slot_booking(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         address = request.POST['address']
#         phone_number = request.POST['phone_number']
#         drone_details = request.POST['drone_details']
#         date = request.POST['date']
#         time = request.POST['time']

#         # Find the specific slot
#         slot = BookingSlot.objects.filter(date=date, time=time, is_booked=False).first()
#         if not slot:
#             return HttpResponse('The selected slot is already booked or unavailable.')

#         # Create booking and mark slot as booked
#         booking = UserBooking.objects.create(
#             name=name, email=email, address=address,
#             phone_number=phone_number, drone_details=drone_details, slot=slot
#         )
#         slot.is_booked = True
#         slot.save()

#         send_mail(
#             'Booking Confirmation',
#             f'Thank you for booking! Your slot on {slot.date} at {slot.time} is confirmed.',
#             'noreply@example.com',
#             [email]
#         )
#         # return redirect('payment_page')
#         return redirect('payment', booking_id=booking.id)


#     slots = BookingSlot.objects.filter(is_booked=False)
#     return render(request, 'slot_booking.html', {'slots': slots})




from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import BookingSlot, UserBooking

def slot_booking(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        drone_details = request.POST['drone_details']
        date = request.POST['date']
        time = request.POST['time']

        # Check if the user has already booked a slot on the selected date
        existing_booking = UserBooking.objects.filter(
            email=email,
            phone_number=phone_number,
            slot__date=date
        ).first()
        if existing_booking:
            return HttpResponse('You can only book one slot per day.', status=400)

        # Find the specific slot
        slot = BookingSlot.objects.filter(date=date, time=time, is_booked=False).first()
        if not slot:
            return HttpResponse('The selected slot is already booked or unavailable.', status=400)

        # Create a booking and set the slot_date field to the slot's date
        booking = UserBooking.objects.create(
            name=name, email=email, address=address,
            phone_number=phone_number, drone_details=drone_details, slot=slot,
            slot_date=slot.date  # Ensure the slot_date is set
        )

        # Redirect to the payment page with the booking ID
        return redirect('payment', booking_id=booking.id)

    slots = BookingSlot.objects.all()
    return render(request, 'slot_booking.html', {'slots': slots})




from django.shortcuts import get_object_or_404

def payment_page(request, booking_id):
    booking = get_object_or_404(UserBooking, id=booking_id)

    if request.method == 'POST':
        # Simulate payment success
        booking.slot.is_booked = True
        booking.slot.save()

        send_mail(
            'Booking Confirmation',
            f'Thank you for your payment! Your slot on {booking.slot.date} at {booking.slot.time} is confirmed.',
            'noreply@example.com',
            [booking.email]
        )
        return HttpResponse('''
       <html>
    <head>
        <style>
            /* Reset and Universal Styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Poppins', Arial, sans-serif;
                background: linear-gradient(135deg, #e0f7fa, #c8e6c9);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: #333;
            }

            .container {
                background: #ffffff;
                padding: 50px 40px;
                border-radius: 15px;
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
                text-align: center;
                max-width: 450px;
                width: 90%;
                animation: fadeIn 1s ease-in-out;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }

            h1 {
                font-size: 2.8rem;
                color: #2ecc71;
                margin-bottom: 20px;
                font-weight: 700;
                text-shadow: 1px 2px 3px rgba(46, 204, 113, 0.5);
            }

            p {
                font-size: 1.2rem;
                color: #555;
                line-height: 1.6;
                margin-top: 15px;
                font-weight: 400;
            }

            .button {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 25px;
                font-size: 1rem;
                font-weight: 600;
                color: #fff;
                background: linear-gradient(135deg, #4caf50, #388e3c);
                border: none;
                border-radius: 25px;
                cursor: pointer;
                box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
                text-decoration: none;
                transition: all 0.3s ease;
            }

            .button:hover {
                background: linear-gradient(135deg, #66bb6a, #43a047);
                box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
                transform: translateY(-3px);
            }

            /* Fade-in Animation */
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* Responsive Design */
            @media (max-width: 600px) {
                h1 {
                    font-size: 2.2rem;
                }

                p {
                    font-size: 1rem;
                }

                .button {
                    font-size: 0.9rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Payment Successful!</h1>
            <p>Your slot is confirmed. Thank you for choosing our service!</p>
            <a href="/" class="button">Back to Home</a>
        </div>
    </body>
</html>


    ''')

    return render(request, 'payment_page.html', {'booking': booking})


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
    available_slots = BookingSlot.objects.filter(date=date, is_booked=False)
    booked_slots = BookingSlot.objects.filter(date=date, is_booked=True)

    available_times = [slot.time.strftime('%H:%M') for slot in available_slots]
    booked_times = [slot.time.strftime('%H:%M') for slot in booked_slots]

    return JsonResponse({'times': available_times, 'bookedSlots': booked_times})



def confirm_payment(request):
    # Your function logic here
    pass



def get_booked_slots(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'Date is required'}, status=400)

    slots = BookingSlot.objects.filter(date=date)
    data = [
        {'time': slot.time.strftime('%H:%M'), 'is_booked': slot.is_booked}
        for slot in slots
    ]
    return JsonResponse({'slots': data})