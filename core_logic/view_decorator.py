from django.shortcuts import render, redirect
from .forms import AddExtendForm, AddIncomeForm
from .models import Wallet, Extend, Income
from account.models import Profile
from decimal import Decimal


def request_check(func):
    def wrapper(request):
        if request.method == "POST":
            if 'btn_extend' in request.POST:
                extend_form = AddExtendForm(request.POST)
                if extend_form.is_valid():
                    user_wallet = Wallet.objects.get(
                        user=Profile.objects.get(user=request.user))
                    if user_wallet.balance - extend_form.cleaned_data['price'] < 0:
                        return render(request, 'core_logic/main_stat.html',
                                      {'active': 'dashboard',
                                                 'extend_form': extend_form,
                                                 'income_form': AddIncomeForm(),
                                                 'wallet': user_wallet,
                                                 'sum_extends': Decimal(sum([x.price for x in Extend.objects.filter(wallet=user_wallet)])),
                                                 'error': True})
                    else:
                        user_wallet.balance = Decimal(
                            user_wallet.balance) - Decimal(extend_form.cleaned_data['price'])
                        user_wallet.save()
                        ex = Extend.objects.create(category=extend_form.cleaned_data['category'],
                                                   price=extend_form.cleaned_data['price'],
                                                   comment=extend_form.cleaned_data['comment'],
                                                   wallet=user_wallet)
                        ex.save()
                        return redirect('/')
            elif 'btn_income' in request.POST:
                income_form = AddIncomeForm(request.POST)
                if income_form.is_valid():
                    user_wallet = Wallet.objects.get(
                        user=Profile.objects.get(user=request.user))
                    user_wallet.balance = Decimal(
                        user_wallet.balance) + Decimal(income_form.cleaned_data['price'])
                    user_wallet.save()
                    inc = Income.objects.create(
                        price=income_form.cleaned_data['price'],
                        wallet=user_wallet)
                    inc.save()
                return redirect('/')
        else:
        	return func(request)
    return wrapper
