#from xml.etree.ElementTree import Comment
from django.contrib import admin

from auctions.models import Bid, User, Watchlist, Winner, auctionListing, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(auctionListing)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Winner)
