from django.db import models


class Trend(models.Model):
    date = models.DateTimeField()
    variable = models.CharField(max_length=100)
    value = models.IntegerField()
