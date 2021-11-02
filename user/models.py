from django.db import models

# Create your models here.
from beer.models import Beer, Category


class User(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=20)
    beers = models.ManyToManyField(Beer)
    categories = models.ManyToManyField(Category)

