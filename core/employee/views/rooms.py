from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from core.forms import RoomForm
from core.models import Room


@login_required
def rooms_page(request):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    rooms = Room.objects.all().order_by('name')

    return render(
        request,
        'employee/rooms/index.html',
        {
            'rooms': rooms,
        },
    )


@login_required
def add_room(request):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    if request.method == 'POST':
        form = RoomForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Room added successfully.',
            )

            return redirect('employee_rooms')

    else:
        form = RoomForm()

    return render(
        request,
        'employee/rooms/add.html',
        {
            'form': form,
        },
    )


@login_required
def edit_room(request, room_id):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    room = get_object_or_404(
        Room,
        id=room_id,
    )

    if request.method == 'POST':
        form = RoomForm(
            request.POST,
            request.FILES,
            instance=room,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Room updated successfully.',
            )

            return redirect('employee_rooms')

    else:
        form = RoomForm(instance=room)

    return render(
        request,
        'employee/rooms/edit.html',
        {
            'form': form,
            'room': room,
        },
    )


@login_required
def delete_room(request, room_id):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    room = get_object_or_404(
        Room,
        id=room_id,
    )

    room.delete()

    messages.success(
        request,
        'Room deleted successfully.',
    )

    return redirect('employee_rooms')