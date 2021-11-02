from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('populate-users', views.populate_users),
    path('populate-users-beers', views.populate_users_beers),
]
