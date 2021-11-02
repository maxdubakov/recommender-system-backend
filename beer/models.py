from django.db import models

# Create your models here.
class Beer(models.Model):
    name = models.CharField(max_length=20)
    number = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=20)
    beers = models.ManyToManyField(Beer)
