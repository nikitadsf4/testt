from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Room, Booking
from django.http import HttpResponse
import datetime
from django.utils import timezone
from calendar import monthrange


def index(request):
    context = {
        "render_string": "Hello, world!"
    }
    return render(request, template_name="booking/index.html", context=context)


def room_list(request):
    rooms = Room.objects.all()
    context = {
        "rooms": rooms,
    }
    return render(request, template_name="booking/rooms_list.html", context=context)


def book_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room-number")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        try:
            room = Room.objects.get(number=room_number)
        except ValueError:
            return HttpResponse(
                "Wrong value for room number!",
                status=400
            )
        except Room.DoesNotExist:
            return HttpResponse(
                "This room number doesn't exist",
                status=404
            )
        booking = Booking.objects.create(
            user=request.user,
            room=room,
            start_time=start_time,
            end_time=end_time
        )
        return redirect("booking-details", pk=booking.id)
    else: 
        return render(request, template_name="booking/booking_form.html")


def booking_details(request, pk):
    try:
        booking = Booking.objects.get(id=pk)
        context = {
            "booking": booking
        }
        return render(request, template_name="booking/booking_details.html", context=context)
    except Booking.DoesNotExist:
        return HttpResponse(
            "This booking doesn't exist",
            status=404
        )


def view_room_availability(request, pk):
    room = get_object_or_404(Room, pk=pk)
    today = timezone.now()
    first_day_of_month = datetime.date(today.year, today.month, 1)
    last_day_of_month = datetime.date(today.year, today.month, monthrange(today.year, today.month)[1])

    bookings = Booking.objects.filter(room=room, start_time__range=(first_day_of_month, last_day_of_month))

    booked_days = {booking.start_time.day for booking in bookings}

    days_of_month = range(1, monthrange(today.year, today.month)[1] + 1)

    context = {
        'room': room,
        'days_of_month': days_of_month,
        'booked_days': booked_days,
        'today': today,
    }
    return render(request, 'booking/room_availability_calendar.html', context)
