from django.contrib.auth.models import AbstractUser
from django.db import models

"""Pseudo-code: at least 3 models apart from users 
- for auction listings (id, status, seller/username) >
- for bids (pk id, fk_auction_listing_id, price, time, username)
- for auction-related comments(pk id, fk_auction_listing_id, comments, username)
- for user, (autoincrement) pk id, username, password
** May have more tables to add 

-- Decide relationships first


- User <> Auction listings / bids / comments -- M-M
- Seperate user_id to a seperate id and username, password, etc.
- auction listings <> bids
"""
class User(AbstractUser):
    pass

class auctionListing(models.Model):
    title = models.CharField(max_length = 99)
    seller = models.CharField(max_length = 49)
    description = models.TextField()
    startingPrice = models.DecimalField(max_digits= 9, decimal_places = 2)
    category = models.CharField(max_length = 49)
    imageLink = models.CharField(max_length = 499, default = None, blank = True, null = True)
    openTime = models.DateTimeField(auto_now_add = True)
    
class Bid(models.Model):
    user = models.CharField(max_length = 49)
    title = models.CharField(max_length = 99)
    listingId = models.IntegerField()
    bid = models.DecimalField(max_digits = 9, decimal_places = 2)

class Comment(models.Model):
    user = models.CharField(max_length = 49)
    comment = models.CharField(max_length = 499)
    listingId = models.IntegerField()
    time = models.DateTimeField(auto_now_add = True)

class Watchlist(models.Model):
    user = models.CharField(max_length = 49)
    listingId = models.IntegerField()

class Winner(models.Model):
    title = models.CharField(max_length = 99, null = True)
    seller = models.CharField(max_length = 49)
    winner = models.CharField(max_length = 49)
    listingId = models.IntegerField()
    finalPrice = models.DecimalField(max_digits = 9, decimal_places = 2)
    