from django.db import models
import jsonfield


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(default='', max_length=10)
    name = models.CharField(default='', max_length=50)
    geolocation_type = models.CharField(default='country', max_length=10)
    country_code = models.CharField(default='', max_length=10)
    supports_region = models.BooleanField(null=True)
    supports_city = models.BooleanField(null=True)


class CountryGroup(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(default='', max_length=50)
    name = models.CharField(default='', max_length=50)
    geolocation_type = models.CharField(default='country_group', max_length=30)
    country_codes = jsonfield.JSONField(null=True)
    is_worldwide = models.BooleanField(null=True)
    supports_region = models.BooleanField(null=True)
    supports_city = models.BooleanField(null=True)
    region = models.CharField(default='', null=True, max_length=50)


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(default='', max_length=50)
    name = models.CharField(default='', max_length=100)
    geolocation_type = models.CharField(default='region', max_length=50)
    country_code = models.CharField(default='', max_length=10)
    country_name = models.CharField(default='', max_length=100)
    supports_region = models.BooleanField(null=True)
    supports_city = models.BooleanField(null=True)


class GeoMarket(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(default='', max_length=50)
    name = models.CharField(default='', max_length=100)
    geolocation_type = models.CharField(default='geo_market', max_length=50)
    country_code = models.CharField(default='', max_length=10)
    supports_region = models.BooleanField(null=True)
    supports_city = models.BooleanField(null=True)


class ElectoralDistrict(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(default='', max_length=50)
    name = models.CharField(default='', max_length=255)
    geolocation_type = models.CharField(default='electoral_district', max_length=50)
    country_code = models.CharField(default='US', max_length=10)
    supports_region = models.BooleanField(null=True)
    supports_city = models.BooleanField(null=True)
