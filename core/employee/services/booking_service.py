from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from core.models import Booking


def mark_past_bookings_completed():

    Booking.objects.filter(
        status__in=['Pending', 'Confirmed'],
        check_out__lt=timezone.localdate(),
    ).update(status='Completed')


def calculate_available_rooms(
    room,
    check_in_date,
    check_out_date,
    exclude_booking_id=None,
):

    overlapping_bookings = Booking.objects.filter(
        room=room,
        status='Confirmed',
        check_in__lt=check_out_date,
        check_out__gt=check_in_date,
    )

    if exclude_booking_id:
        overlapping_bookings = overlapping_bookings.exclude(
            id=exclude_booking_id,
        )

    return room.total_quantity - overlapping_bookings.count()


def calculate_booking_total(
    room,
    check_in_date,
    check_out_date,
):

    nights = (check_out_date - check_in_date).days

    if nights <= 0:
        nights = 1

    return room.price * nights


@transaction.atomic
def create_walkin_booking(form):

    booking = form.save(commit=False)

    available = calculate_available_rooms(
        booking.room,
        booking.check_in,
        booking.check_out,
    )

    if available <= 0:
        raise ValueError(
            'Selected room is not available for those dates.'
        )

    booking.booking_type = 'Walk-in'

    booking.status = 'Confirmed'

    booking.total_price = calculate_booking_total(
        booking.room,
        booking.check_in,
        booking.check_out,
    )

    booking.save()

    return booking


def cancel_booking(booking):

    today = timezone.localdate()

    if booking.check_in < today:
        raise ValueError(
            'Past reservations cannot be cancelled.'
        )

    booking.status = 'Cancelled'

    booking.save()