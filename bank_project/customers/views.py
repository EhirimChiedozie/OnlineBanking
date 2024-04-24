from django.shortcuts import render, redirect
from .forms import AccountOpeningForm
from .models import Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransferForm
from customers.models import Transfer
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

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

@login_required
def confirm_logout(request):
    return render(request, 'customers/confirm_logout.html')



@login_required
def make_transfer_request(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            receiver_account = form.cleaned_data.get('receiver_account')
            request.session['receiver_account'] = receiver_account
            amount = float(form.cleaned_data.get('amount'))
            request.session['amount'] = amount
            receiver = Customer.objects.filter(account_number=receiver_account).first()
            return render(request, 'customers/confirm_transfer_details.html', {'amount':amount, 'receiver':receiver})
    else: 
        form = TransferForm()
    context = {'form':form}
    return render(request, 'customers/make_transfer_request.html', context=context)


@login_required
def confirm_transfer_details(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            sender = Customer.objects.filter(account_number=request.user.account_number).first()
            amount = request.session.get('amount')
            receiver_account = request.session.get('receiver_account')
            receiver = Customer.objects.filter(account_number=receiver_account).first()
            receiver_name = receiver.first_name.upper() + ' ' + receiver.last_name.upper()
            if receiver:
                if amount > 0:
                    if receiver.account_number == sender.account_number:
                        messages.error(request, 'You cannot transfer to yourself')
                    else:
                        if sender.account_balance <= amount:
                            messages.warning(request, 'Insufficient funds')
                        else:
                            return redirect('execute_transfer')
                else:
                    messages.warning(request, 'Invalid amount')
            else:
                messages.warning(request, "Invalid account number provided".title())

            
    else:
        form = TransferForm()
    context = {'form':form}
    return render(request, 'customers/confirm_transfer_details.html', context=context)

@login_required
def execute_transfer(request):
    sender = Customer.objects.filter(account_number=request.user.account_number).first()
    amount = request.session.get('amount')
    sender.account_balance -= amount
    receiver_account = request.session.get('receiver_account')
    receiver = Customer.objects.filter(account_number=receiver_account).first()
    receiver.account_balance += amount
    sender.save()
    receiver.save()
    transfer = Transfer(user=request.user, receiver_account=receiver, amount=amount)
    transfer.save()
    messages.success(request, f"Transfer to {receiver.first_name} {receiver.last_name} was successful")
    return redirect('bankapp_home')


class CustomerStatementView(ListView, LoginRequiredMixin):
    models = Transfer
    context_object_name = 'transfers'
    template_name = 'customers/statement.html'

    def get_queryset(self):
        return Transfer.objects.filter(Q(user=self.request.user) | Q(receiver_account=self.request.user.email)).order_by('-date')