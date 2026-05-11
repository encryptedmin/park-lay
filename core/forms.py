from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    Room,
    Booking,
    GCashAccount,
)


User = get_user_model()


class StyledFormMixin:

    def apply_auth_styling(self):

        for field in self.fields.values():

            existing_classes = field.widget.attrs.get(
                'class',
                '',
            )

            field.widget.attrs.update({
                'class': f'{existing_classes} auth-input'.strip(),
                'placeholder': field.label,
            })


class BookingDateValidationMixin:

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        today = timezone.localdate().isoformat()

        for field_name in ['check_in', 'check_out']:

            if field_name in self.fields:

                self.fields[field_name].widget.attrs.update({
                    'min': today,
                })

    def clean(self):

        cleaned_data = super().clean()

        check_in = cleaned_data.get('check_in')

        check_out = cleaned_data.get('check_out')

        if (
            check_in
            and
            check_out
            and
            check_out <= check_in
        ):
            raise forms.ValidationError(
                'Check-out date must be after check-in date.'
            )

        if (
            check_in
            and
            check_in < timezone.localdate()
        ):
            raise forms.ValidationError(
                'Check-in date cannot be in the past.'
            )

        return cleaned_data


class CustomerRegistrationForm(
    StyledFormMixin,
    forms.ModelForm,
):

    password = forms.CharField(
        widget=forms.PasswordInput(),
    )

    class Meta:

        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        user.is_customer = True

        if commit:
            user.save()

        return user


class CustomerProfileForm(
    StyledFormMixin,
    forms.ModelForm,
):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )

    class Meta:

        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        user.is_customer = True

        user.is_employee = False

        if commit:
            user.save()

        return user


class CustomerForm(
    StyledFormMixin,
    forms.ModelForm,
):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()

    def save(self, commit=True):

        user = super().save(commit=False)

        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        user.is_customer = True

        if commit:
            user.save()

        return user


class RoomForm(
    StyledFormMixin,
    forms.ModelForm,
):

    class Meta:

        model = Room

        fields = [
            'name',
            'inclusions',
            'price',
            'total_quantity',
            'image',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()


class GCashAccountForm(
    StyledFormMixin,
    forms.ModelForm,
):

    class Meta:

        model = GCashAccount

        fields = [
            'account_name',
            'account_number',
            'qr_code',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()


class OnlineBookingForm(
    StyledFormMixin,
    BookingDateValidationMixin,
    forms.ModelForm,
):

    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    check_out = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    class Meta:

        model = Booking

        fields = [
            'check_in',
            'check_out',
            'gcash_reference',
            'payment_proof',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()


class WalkInBookingForm(
    StyledFormMixin,
    BookingDateValidationMixin,
    forms.ModelForm,
):

    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'id_room',
            }
        ),
    )

    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    check_out = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    class Meta:

        model = Booking

        fields = [
            'guest_name',
            'room',
            'check_in',
            'check_out',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()


class BookingUpdateForm(
    StyledFormMixin,
    BookingDateValidationMixin,
    forms.ModelForm,
):

    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    check_out = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    class Meta:

        model = Booking

        fields = [
            'guest_name',
            'room',
            'check_in',
            'check_out',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.apply_auth_styling()