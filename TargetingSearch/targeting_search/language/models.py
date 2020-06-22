from django.db import models

class LanguageModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    key = models.IntegerField(blank=True)
