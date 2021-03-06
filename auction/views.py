from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .models import Auction, WatchList, Bid
from antiques.models import Antiques
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from auctioneer.config import pagination
from .forms import BidForm


@login_required(login_url='/accounts/login')
def get_all_auctions(request):
    """
    Show all current auctions
    """
    user = request.user
    auction = Auction.objects.all()
    pages = pagination(request, auction, 4)
    watchlist = WatchList.objects.filter(user=user)

    context = {
        'items': pages[0],
        'page_range': pages[1],
        'auction': auction,
        'watchlist': watchlist
    }
    return render(request, "showallauctions.html", context)

@login_required(login_url='/accounts/login')
def get_specific_auction(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    context = {
        'auction': auction
    }

    return render(request, 'auction.html', context)

@login_required(login_url='/accounts/login')
def bid(request, pk):
    """
    Allow the user to join the Auction
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            auction = get_object_or_404(Auction, pk=pk)
            if timezone.now() >= auction.time_starting and timezone.now() < auction.time_ending:
                bid = get_object_or_404(Bid, pk=pk)
                the_bid = Decimal(request.POST.get('bid'))
                    
                if auction.current_leader >= the_bid:
                    print('This bid is not high enough')
                    messages.error(request, "This bid is not high enough")

                else:
                    auction.current_leader = the_bid
                    auction.winning_bidder = request.user
                    bid.new_bid = the_bid
                    bid.antiques = auction.antiques
                    bid.auction = auction
                    bid.user = request.user
                    bid.auction.number_of_bids += 1
                    bid.bid_time = timezone.now()
                    bid.save()
                    auction.save()
                    messages.success(request, "Your bid amount has been updated!")

            else:
                messages.error(request, "Sorry, this item is either no longer up for auction or hasnt been put up yet")
   
        else:
            messages.error(request, "You must be registered to bid")
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login')
def add_to_watch_list(request, pk):
    """
    Adds an auction to the users watchlist, not working currently
    """
    auction = Auction.objects.filter(pk=pk)
    watching = WatchList.objects.filter(pk=pk)
    if not watching:
        watchlist_item = WatchList()
        watchlist_item.auction = auction[0]
        watchlist_item.user = request.user
        watchlist_item.save()
    else:
        watching.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/accounts/login')
def display_watch_and_bids(request, user):
    """
    Display the watchlist on watchlist.html
    """

    user = request.user
    watchlist = WatchList.objects.filter(user=user)
    bids = Bid.objects.filter(user=user)

    context = {
        'watchlist': watchlist,
        'bids': bids
    }
    return render(request, "watchlist.html", context)
