from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class AccountOpeningForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'phonenumber', 'password1', 'password2']