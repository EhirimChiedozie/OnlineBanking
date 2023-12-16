from django.shortcuts import render, redirect
from .forms import AccountOpeningForm, TransferForm
from .models import Customer, Transfers
from django.contrib.auth import hashers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

@login_required
def profile(request):
    return render(request, 'customers/profile.html') 

def confirm_logout(request):
    return render(request, 'customers/confirm_logout.html')

def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data.get('receiver_account')
            amount = float(form.cleaned_data.get('amount'))
            receiver = Customer.objects.filter(account_number=account).first()
            sender = Customer.objects.filter(account_number=request.user.account_number).first()
            if receiver:
                if receiver.account_number == sender.account_number:
                    messages.error(request, 'You cannot transfer to yourself')
                else:
                    if receiver.account_balance <= amount:
                        messages.warning(request, 'Insufficient funds')
                    else:
                        sender.account_balance -= amount
                        receiver.account_balance += amount
                        sender.save()
                        receiver.save()
                        messages.success(request, f"Transfer to {receiver.first_name} {receiver.last_name} was successful")
                        return redirect('bankapp_home')
            else:
                messages.warning(request, "Invalid account number provided".title())
    else:
        form = TransferForm()
    context = {'form':form}
    return render(request, 'customers/transfer.html', context=context)