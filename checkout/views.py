from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from auction.models import Auction
from antiques.models import Antiques
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def success(request):
    """
    Render the success page after payment
    """
    user = request.user
    context = {
        'user': user
    }
    return render(request, "success.html", context)



@login_required(login_url='/accounts/login')
def checkout_auction(request, pk):
    """
    Allow the user to make a payment after successfully winning an auction
    """
    user = get_object_or_404(User, pk=pk)
    auction = get_object_or_404(Auction, pk=pk)
    total = auction.current_leader
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()

            total = auction.current_leader
            order_line_item = OrderLineItem(
                order=order,
                auction=auction,
            )
            order_line_item.save()

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                auction.money_collected = True
                auction.antiques.bought = True
                auction.auction_expired = True
                auction.save()
                print("Are you working?")
                return redirect('checkout:success')
            else:
                messages.success(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()

    context = {
        'auction': auction,
        'total': total,
        'order_form': order_form,
        'payment_form': payment_form,
        'publishable': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "auction-checkout.html", context)


@login_required(login_url='/accounts/login')
def buy_now_checkout(request, pk):
    """
    Allow the user to "buy-now"
    """
    auction = get_object_or_404(Auction, pk=pk)
    total = auction.antiques.buy_now_price
    print('why arent you working1')
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        print('why arent you working2')
        
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            order_line_item = OrderLineItem(
                order=order,
                auction=auction,
            )
            order_line_item.save()
            order_line_item.save()
            print('why arent you working3')

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
                print('why arent you working4')
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.success(request, "You have successfully paid")
                auction.money_collected = True
                auction.antiques.bought = True
                auction.auction_expired = True
                auction.save()
                print('why arent you working5')
                return redirect(reverse('products:antiques'))
            else:
                messages.error(request, "Unable to take payment")
                
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        print('why arent you working6')

    context = {
        'auction': auction,
        'total': total,
        'order_form': order_form,
        'payment_form': payment_form,
        'publishable': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, "buy-now.html", context)
