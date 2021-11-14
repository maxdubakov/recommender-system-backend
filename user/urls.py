from django.urls import path
from . import views


urlpatterns = [
    path('new', views.post_user),
    path('new-categories', views.post_user_categories),
    path('new-beers', views.post_user_beers),
    path('get-beers', views.get_user_beers),
    path('predict', views.predict_beers),
    path('train', views.train)
]
