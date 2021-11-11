from django.urls import path
from . import views

urlpatterns = [
    path('get-categories', views.get_categories),

    # DEVELOPMENT ENDPOINTS
    path('populate-beers', views.populate_beers),
    path('delete-beers', views.delete_beers),
    path('populate-categories', views.populate_categories),
    path('delete-categories', views.delete_categories),
    path('populate-beers-to-categories', views.populate_beer_to_categories),
]
