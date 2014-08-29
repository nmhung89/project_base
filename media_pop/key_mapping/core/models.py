from django.db import models

class KeyMapping(models.Model):
    SpecialKey = models.CharField(max_length=2)
    Key = models.CharField(max_length=2)
    Message = models.CharField(max_length=100)