from django.urls import path

from .views.dashboard import employee_dashboard

from .views.bookings import (
    bookings_page,
    walkin_booking,
    confirm_booking,
    reject_booking,
    cancel_active_booking,
)

from .views.rooms import (
    rooms_page,
    add_room,
    edit_room,
    delete_room,
)

from .views.customers import (
    customers_page,
    add_customer,
    edit_customer,
    delete_customer,
)

from .views.payments import payments_page

urlpatterns = [

    path(
    'bookings/<int:booking_id>/cancel/',
    cancel_active_booking,
    name='cancel_active_booking',
),

    path(
        'dashboard/',
        employee_dashboard,
        name='employee_dashboard',
    ),

    path(
        'bookings/',
        bookings_page,
        name='employee_bookings',
    ),

    path(
        'bookings/walk-in/',
        walkin_booking,
        name='walkin_booking',
    ),

    path(
        'bookings/<int:booking_id>/confirm/',
        confirm_booking,
        name='confirm_booking',
    ),

    path(
        'bookings/<int:booking_id>/reject/',
        reject_booking,
        name='reject_booking',
    ),

    path(
        'rooms/',
        rooms_page,
        name='employee_rooms',
    ),

    path(
        'rooms/add/',
        add_room,
        name='add_room',
    ),

    path(
        'rooms/<int:room_id>/edit/',
        edit_room,
        name='edit_room',
    ),

    path(
        'rooms/<int:room_id>/delete/',
        delete_room,
        name='delete_room',
    ),

    path(
        'customers/',
        customers_page,
        name='employee_customers',
    ),

    path(
        'customers/add/',
        add_customer,
        name='add_customer',
    ),

    path(
        'customers/<int:customer_id>/edit/',
        edit_customer,
        name='edit_customer',
    ),

    path(
        'customers/<int:customer_id>/delete/',
        delete_customer,
        name='delete_customer',
    ),

    path(
        'payments/',
        payments_page,
        name='employee_payments',
    ),
]