from __future__ import unicode_literals

from django.db import models


class City(models.Model):
    city = models.CharField(max_length=30, primary_key=True)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    temperature = models.CharField(max_length=30)
