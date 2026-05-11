from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from core.forms import CustomerForm
from core.models import User


@login_required
def customers_page(request):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    customers = User.objects.filter(
        is_customer=True,
    ).order_by(
        'last_name',
        'first_name',
    )

    return render(
        request,
        'employee/customers/index.html',
        {
            'customers': customers,
        },
    )


@login_required
def add_customer(request):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    if request.method == 'POST':

        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)

            customer.is_customer = True

            customer.save()

            messages.success(
                request,
                'Customer created successfully.',
            )

            return redirect('employee_customers')

    else:
        form = CustomerForm()

    return render(
        request,
        'employee/customers/add.html',
        {
            'form': form,
        },
    )


@login_required
def edit_customer(request, customer_id):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    customer = get_object_or_404(
        User,
        id=customer_id,
    )

    if request.method == 'POST':

        form = CustomerForm(
            request.POST,
            instance=customer,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Customer updated successfully.',
            )

            return redirect('employee_customers')

    else:
        form = CustomerForm(instance=customer)

    return render(
        request,
        'employee/customers/edit.html',
        {
            'form': form,
            'customer': customer,
        },
    )


@login_required
def delete_customer(request, customer_id):
    if not getattr(request.user, 'is_employee', False):
        return redirect('customer_home')

    customer = get_object_or_404(
        User,
        id=customer_id,
    )

    customer.delete()

    messages.success(
        request,
        'Customer deleted successfully.',
    )

    return redirect('employee_customers')