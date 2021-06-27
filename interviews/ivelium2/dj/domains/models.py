from django.db import models


class Domain(models.Model):
    name = models.CharField(primary_key=True)
    date_registered = models.PositiveSmallIntegerField()
    date_free = models.PositiveSmallIntegerField()
    last_seen = models.PositiveSmallIntegerField()
    registrator = models.CharField()


class Name(models.Model):
    origin_name = models.CharField(primary_key=True)
    decoded_name = models.CharField()


class Order(models.Model):
    # user = models.ForeignKey()
    name = models.ForeignKey(Name)
    date_free = models.PositiveSmallIntegerField()
