from django.urls import path
from . import views

urlpatterns = [
    path('populate-all', views.populate_all),
    path('delete-all', views.delete_all),
]
