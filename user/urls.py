from django.urls import path
from . import views

urlpatterns = [
    path('new-user', views.post_user),
    path('new-user-categories', views.post_user_categories),
    path('new-user-beers', views.post_user_beers),
    path('get-user-beers', views.get_user_beers),
    path('predict-beers', views.predict_beers),

    # DEVELOPMENT ENDPOINTS
    path('populate-users', views.populate_users),
    path('populate-users-beers', views.populate_users_beers),
    path('get-user-beers/<slug:slug>', views.get_beers_for_user),
]
