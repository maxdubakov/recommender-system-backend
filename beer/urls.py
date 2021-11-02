from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get-beers', views.get_beers),
    path('get-beers/<slug:slug>', views.get_beers_with_category),
    path('post-beers', views.post_beers),
    path('populate-beers', views.populate_beers),
    path('delete-beers', views.delete_beers),
    path('populate-categories', views.populate_categories),
    path('delete-categories', views.delete_categories),
    path('populate-beers-to-categories', views.populate_beer_to_categories),
]
