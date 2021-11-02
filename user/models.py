from django.db import models

# Create your models here.
from beer.models import Beer, Category


class User(models.Model):
    name = models.CharField(max_length=20)
    beers = models.ManyToManyField(Beer)
    categories = models.ManyToManyField(Category)

