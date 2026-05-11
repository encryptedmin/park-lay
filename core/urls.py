from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.customer_home, name='customer_home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('my-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('rooms/', views.rooms_page, name='rooms_page'),

    path('employee/', include('core.employee.urls')),
]