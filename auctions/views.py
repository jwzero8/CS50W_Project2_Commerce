from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from annoying.functions import get_object_or_None
from .models import User, Bid, Watchlist, auctionListing, Comment, Winner

# error? danger? >> msg type
# listing/ auctionListing?
def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                "messageType": "error"
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                "messageType": "error"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "messageType": "error"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url = '/login')
def dashboard(request):
    winners = Winner.objects.filter(winner = request.user.username)  
    list = Watchlist.objects.filter(user = request.user.username)
    present = False
    productList = []
    
    if list:
        present = True
        for item in list:
            product = auctionListing.objects.get(id = item.listingId)
            productList.append()
    
    print(productList)
    return render(request, "auctions/dashboard.html", {
        "productList": productList,
        "present": present,
        "products": winners 
    })
    
@login_required(login_url = '/login')
def activeListing(request):
    products = auctionListing.objects.all()
    empty = False
    if len(products) != 0:
        empty = False 
    else:
        empty = True
    
    return render(request, "auctions/activelisting.html", {
        "products": products,
        "empty": empty
    })

@login_required(login_url = '/login')
def createLisitng(request):
    if request.method == "GET":
        return render(request, "auctions/createlisitng.html")
    
    else:
        request.method == "POST"
        item = auctionListing()
        item.seller = request.user.username
        item.title = request.POST.get("title")
        item.description = request.POST.get("description")
        item.category = request.POST.get("category")
        item.startingPrice = request.POST.get("startingPrice")
        
        if request.POST.get("imageLink"):
            item.imageLink = request.POST.get("imageLink")
        
        # a Troll meme image
        else: 
            item.imageLink = "https://cdn.vox-cdn.com/thumbor/FOIV1c1Eq9Y1HQq-Sn1RgReLp0E=/0x0:735x500/920x613/filters:focal(310x192:426x308):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/66727168/image.0.png"
        
        item.save()
        products = auctionListing.objects.all()
        empty = False
        if len(products) != 0:
            empty = False 
        
        else:
            empty = True
        
        return render(request, "auctions/activelisting.html", {
            "products": products,
            "empty": empty
        })

@login_required(login_url= '/login')
def categories(request):
    return render(request, "auctions/categories.html")

@login_required(login_url= '/login')
def viewListing(request, productId):
    comments = Comment.objects.filter(listingId=productId)
    if request.method == "GET":
        product = auctionListing.objects.get(id=productId)
        added = Watchlist.objects.filter(listingId = productId, user = request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments
        })
    
    else:
        request.method == "POST"
        item = auctionListing.objects.get(id = productId)
        newbid = float(request.POST.get("newbid"))
        
        if item.startingPrice >= newbid:
            product = auctionListing.objects.get(id = productId)
            message = "Your offer should be higher than the current quote!"
            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "messageType": "error",
                "message": message,
                "comments": comments
            })
        
        else:
            item.startingPrice = newbid
            item.save()
            bidobject = Bid.objects.filter(listingId=productId)
            if bidobject:
                bidobject.delete()
            object = Bid()
            object.user = request.user.username
            object.title = item.title
            object.listingId = productId
            object.bid = newbid
            object.save()
            product = auctionListing.objects.get(id=productId)
            message = "You have place the bid!"
            return render(request, "auctions/viewlisting.html", {
                "product": product,
                "messageType": "success",
                "message": message,
                "comments": comments 
            })
    
@login_required(login_url= '/login')
def addWatchlist(request, productId):
    object = Watchlist.objects.filter(listingId = productId, user = request.user.username)
    comments = Comment.objects.filter(listingId = productId)
    
    if object:
        object.delete()
        
        product = auctionListing.objects.get(id = productId)
        added = Watchlist.objects.filter(listingId = productId, user=request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments
        })
        
    else:
        object = Watchlist()
        object.user = request.user.username 
        object.listingId = productId
        object.save()
        product = auctionListing.objects.get(id = productId)
        added = Watchlist.objects.filter(listingId = productId, user = request.user.username)
        return render(request, "auctions/viewlisting.html", {
            "product": product,
            "added": added,
            "comments": comments
        })

@login_required(login_url= '/login')
def addComment(request, productId):
    object = Comment()
    object.comment = request.POST.get("comment")
    object.user = request.user.username
    object.listingId = productId
    object.save()
    
    # printcomments??
    
    comments = Comment.objects.filter(listingId = productId)
    product = auctionListing.objects.get(id = productId)
    added = Watchlist.objects.filter(listingId = productId, user = request.user.username)
    return render(request, "auctions/viewlisting.html", {
        "product": product,
        "added": added,
        "comments": comments
    })
    
@login_required(login_url= '/login')
def category(request, categoryInput):
    # categ ~ categoryInput
    categoryProducts = auctionListing.objects.filter(category = categoryInput)
    empty = False
    if len(categoryProducts) != 0:
        empty = False
    
    else: 
        empty = True
    
    return render(request, "auctions/category.html", {
        "category": categoryInput,
        "empty": empty,
        "products": categoryProducts
    })
    
@login_required(login_url= '/login')
def closeBid(request, productId):
    winObject = Winner()
    listObject = auctionListing.objects.get(id = product_id)
    object = get_object_or_None(Bid, listingId = productId)
    if not object:
        message = "Deleting bid."
        messageType = "error"
    
    else: 
        bidObject = Bid.objects.get(listingId = productId)
        winObject.seller = request.user.username
        winObject.winner = bidObject.user
        winObject.listingId = productId
        winObject.finalPrice = bidObject.bid
        winObject.title = bidObject.title
        winObject.save()
        
        message = "Bid closed"
        messageType = "success"
        bidObject.delete()
    
    # actually this section can be done by adding on-delete cascade, but I am too dumb and not so sure so just forget about it
    if Watchlist.objects.filter(listingId = productId):
        watchObject = Watchlist.objects.filter(listingId = productId)
        watchObject.delete()
    
    if Comment.objects.filter(listingId = productId):
        commentObject = Comment.objects.filter(listingId = productId)
        commentObject.delete()
    
    listObject.delete()
    
    winners = Winner.objects.all()
    
    empty = False 
    
    if len(winners) != 0:
        empty = False 
    
    else:
        return render(request, "auctions.closedlisting.html", {
            "products": winners,
            "empty": empty,
            "message": message,
            "messageType": messageType
        })
        
@login_required(login_url= '/login')
def closedListing(request):
    winners = Winner.objects.all()
    empty = False
    
    if len(winners) != 0:
        empty = False
    
    else:
        empty = True
        return render(request, "auctions/closedlisting.html", {
            "products": winners,
            "empty": empty
        })

