from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .forms import OnlineBookingForm, WalkInBookingForm
from .models import Booking, Room, User
from .views import mark_past_bookings_completed


class BookingDateRulesTests(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.room = Room.objects.create(
            name='Deluxe',
            inclusions='WiFi',
            price=Decimal('1200.00'),
            total_quantity=2,
            image='rooms/test.jpg',
        )
        self.customer = User.objects.create_user(
            username='customer',
            password='pass12345',
            is_customer=True,
        )

    def test_online_booking_rejects_past_check_in(self):
        form = OnlineBookingForm(data={
            'check_in': self.today - timedelta(days=1),
            'check_out': self.today + timedelta(days=1),
            'gcash_reference': 'ABC123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Check-in date cannot be in the past.', form.errors.as_text())

    def test_walkin_booking_rejects_past_check_in(self):
        form = WalkInBookingForm(data={
            'guest_name': 'Walk In Guest',
            'room': self.room.id,
            'check_in': self.today - timedelta(days=1),
            'check_out': self.today + timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Check-in date cannot be in the past.', form.errors.as_text())

    def test_past_active_booking_is_marked_completed(self):
        booking = Booking.objects.create(
            customer=self.customer,
            guest_name='Customer',
            room=self.room,
            check_in=self.today - timedelta(days=3),
            check_out=self.today - timedelta(days=1),
            total_price=Decimal('2400.00'),
            status='Confirmed',
        )

        updated = mark_past_bookings_completed()
        booking.refresh_from_db()

        self.assertEqual(updated, 1)
        self.assertEqual(booking.status, 'Completed')

    def test_future_booking_can_be_cancelled(self):
        booking = Booking.objects.create(
            customer=self.customer,
            guest_name='Customer',
            room=self.room,
            check_in=self.today + timedelta(days=1),
            check_out=self.today + timedelta(days=2),
            total_price=Decimal('1200.00'),
            status='Confirmed',
        )

        self.assertTrue(booking.can_cancel)

    def test_cancel_view_marks_past_booking_completed(self):
        booking = Booking.objects.create(
            customer=self.customer,
            guest_name='Customer',
            room=self.room,
            check_in=self.today - timedelta(days=2),
            check_out=self.today - timedelta(days=1),
            total_price=Decimal('1200.00'),
            status='Confirmed',
        )
        self.client.login(username='customer', password='pass12345')

        self.client.post(reverse('cancel_booking', args=[booking.id]))
        booking.refresh_from_db()

        self.assertEqual(booking.status, 'Completed')
