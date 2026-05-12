from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.customer_home,
        name='customer_home',
    ),

    path(
        'login/',
        views.login_view,
        name='login',
    ),

    path(
        'register/',
        views.register_view,
        name='register',
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout',
    ),

    path(
        'rooms/',
        views.rooms_page,
        name='rooms_page',
    ),

    path(
        'availability/',
        views.room_availability_api,
        name='room_availability_api',
    ),

    path(
        'book/<int:room_id>/',
        views.book_room,
        name='book_room',
    ),

    path(
        'dashboard/',
        views.customer_dashboard,
        name='customer_dashboard',
    ),

    path(
        'booking/<int:booking_id>/edit/',
        views.edit_booking,
        name='edit_booking',
    ),

    path(
        'booking/<int:booking_id>/cancel/',
        views.cancel_booking,
        name='cancel_booking',
    ),

    path(
        'employee/dashboard/',
        views.employee_dashboard,
        name='employee_dashboard',
    ),
    path(
    'employee/payments/',
    views.payment_information,
    name='payment_information',
    ),
    path(
        'employee/booking/<int:booking_id>/confirm/',
        views.confirm_booking,
        name='confirm_booking',
    ),

    path(
        'employee/booking/<int:booking_id>/reject/',
        views.reject_booking,
        name='reject_booking',
    ),

    path(
        'employee/customers/',
        views.manage_customers,
        name='manage_customers',
    ),

    path(
        'employee/customers/add/',
        views.add_customer,
        name='add_customer',
    ),

    path(
        'employee/customers/<int:customer_id>/edit/',
        views.edit_customer,
        name='edit_customer',
    ),

    path(
        'employee/customers/<int:customer_id>/delete/',
        views.delete_customer,
        name='delete_customer',
    ),

    path(
        'employee/rooms/add/',
        views.add_room,
        name='add_room',
    ),

    path(
        'employee/rooms/<int:room_id>/edit/',
        views.edit_room,
        name='edit_room',
    ),

    path(
        'employee/walkin/',
        views.walkin_booking,
        name='walkin_booking',
    ),

    path(
        'employee/gcash/add/',
        views.add_gcash_account,
        name='add_gcash_account',
    ),

    path(
        'employee/gcash/<int:account_id>/edit/',
        views.edit_gcash_account,
        name='edit_gcash_account',
    ),

    path(
        'employee/gcash/<int:account_id>/delete/',
        views.delete_gcash_account,
        name='delete_gcash_account',
    ),
]