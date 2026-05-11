from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from core.models import Booking
from core.models import GCashAccount


@login_required
def payments_page(request):
    if not request.user.is_employee:
        return redirect('customer_home')

    bookings = Booking.objects.exclude(
        payment_proof='',
    ).order_by('-created_at')

    gcash_accounts = GCashAccount.objects.all().order_by('-created_at')

    return render(
        request,
        'employee/payments/index.html',
        {
            'bookings': bookings,
            'gcash_accounts': gcash_accounts,
        },
    )