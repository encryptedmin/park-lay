from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from core.models import Booking
from core.models import Room
from core.models import User

from core.employee.services.booking_service import mark_past_bookings_completed


@login_required
def employee_dashboard(request):
    if not request.user.is_employee:
        return redirect('customer_home')

    mark_past_bookings_completed()

    context = {
        'total_bookings': Booking.objects.count(),
        'pending_bookings': Booking.objects.filter(status='Pending').count(),
        'confirmed_bookings': Booking.objects.filter(status='Confirmed').count(),
        'completed_bookings': Booking.objects.filter(status='Completed').count(),
        'total_rooms': Room.objects.count(),
        'total_customers': User.objects.filter(is_customer=True).count(),
        'recent_bookings': Booking.objects.select_related(
            'room',
            'customer',
        ).order_by('-created_at')[:10],
    }

    return render(
        request,
        'employee/dashboard/index.html',
        context,
    )