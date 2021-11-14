from django.urls import path
from . import views


urlpatterns = [
    path('get-categories', views.get_categories)
]
