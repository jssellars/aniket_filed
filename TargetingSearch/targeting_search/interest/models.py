from django.db import models


class RawInterest(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(default='', max_length=50)
    name = models.CharField(default='', max_length=100)
    type = models.CharField(default='', max_length=50)
    path = models.TextField(null=True)
    description = models.TextField(default='', max_length=255)
    audience_size = models.BigIntegerField(blank=True, null=True)
    real_time_cluster = models.BooleanField(blank=True, null=True)
