from django.shortcuts import render, redirect
from .forms import AccountOpeningForm
from .models import Customer
from django.contrib import messages

# Create your views here.

def open_account(request):
    if request.method == 'POST':
        form = AccountOpeningForm(request.POST)
        if form.is_valid():
            list_phonenumber = list(form.cleaned_data.get('phonenumber'))
            list_account_number = list_phonenumber[len(list_phonenumber) - 10 : ]
            account_number = ''.join(list_account_number)
            form.save()
            customer = Customer.objects.get(phonenumber=form.cleaned_data.get('phonenumber'))
            customer.account_number = account_number
            customer.save()
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            messages.success(request, f'Account created for {first_name} {last_name} was successful')
            return redirect('bankapp_home')
    else:
        form = AccountOpeningForm()
    return render(request, 'customers/open_account.html', {'form':form})