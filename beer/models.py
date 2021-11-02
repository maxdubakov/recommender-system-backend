from django.db import models

# Create your models here.
class Beer(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=20)


class Category(models.Model):
    name = models.CharField(max_length=20)
    beers = models.ManyToManyField(Beer)
