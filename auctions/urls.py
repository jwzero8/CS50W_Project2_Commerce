from django.urls import path

from . import views


# name is for HTML file
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activelisting", views.activeListing, name="activeListing"),
    path("createlisting", views.createLisitng, name="createLisitng"),
    path("viewlisting/<int:productId>", views.viewListing, name="viewListing"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categoryInput>", views.category, name="category"),
    path("addwatchlist/<int:productId>", views.addWatchlist, name="addWatchlist"),
    path("addcomment/<int:productId>", views.addComment, name="addComment"),
    path("closebid/<int:productId>", views.closeBid, name="closeBid"),
    path("closedlisting", views.closedListing, name="closedListing")
]
