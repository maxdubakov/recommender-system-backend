from django.db import models

from beer.models import Beer, Category


class User(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=20, db_index=True)
    beers = models.ManyToManyField(Beer, through='UserBeer')
    categories = models.ManyToManyField(Category)


class UserBeer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
