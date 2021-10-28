from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get-beers', views.get_beers),
    path('post-beers', views.post_beers),
]
