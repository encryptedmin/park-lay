from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from core.forms import WalkInBookingForm
from core.models import Booking

from core.employee.services.booking_service import (
    create_walkin_booking,
    mark_past_bookings_completed,
    cancel_booking,
)


@login_required
def bookings_page(request):

    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    mark_past_bookings_completed()

    bookings = Booking.objects.select_related(
        'room',
        'customer',
    ).order_by('-created_at')

    return render(
        request,
        'employee/bookings/index.html',
        {
            'bookings': bookings,
        },
    )


@login_required
def walkin_booking(request):

    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    if request.method == 'POST':

        form = WalkInBookingForm(request.POST)

        if form.is_valid():

            try:

                booking = create_walkin_booking(form)

                messages.success(
                    request,
                    f'Walk-in booking for {booking.guest_name} created successfully.',
                )

                return redirect('employee_bookings')

            except ValueError as error:

                messages.error(
                    request,
                    str(error),
                )

        else:

            messages.error(
                request,
                'Please correct the form errors.',
            )

    else:

        form = WalkInBookingForm()

    return render(
        request,
        'employee/bookings/walkin.html',
        {
            'form': form,
        },
    )


@login_required
def confirm_booking(request, booking_id):

    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
    )

    booking.status = 'Confirmed'

    booking.save()

    messages.success(
        request,
        'Booking confirmed.',
    )

    return redirect('employee_bookings')


@login_required
def reject_booking(request, booking_id):

    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
    )

    booking.status = 'Rejected'

    booking.save()

    messages.success(
        request,
        'Booking rejected.',
    )

    return redirect('employee_bookings')


@login_required
def cancel_active_booking(request, booking_id):

    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    booking = get_object_or_404(
        Booking,
        id=booking_id,
    )

    try:

        cancel_booking(booking)

        messages.success(
            request,
            'Reservation cancelled successfully.',
        )

    except ValueError as error:

        messages.error(
            request,
            str(error),
        )

    return redirect('employee_bookings')