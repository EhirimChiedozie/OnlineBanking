from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Transfer
from django import forms

class AccountOpeningForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'phonenumber', 'password1', 'password2']


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['receiver_account', 'amount']