from django.db import models

SPECIAL_KEYS = [('CTRL', 'CTRL'), ('ALT', 'ALT')]

class KeyMapping(models.Model):
    class Meta:
        unique_together = ('SpecialKey', 'Key')
        
    SpecialKey = models.CharField(max_length=5, choices=SPECIAL_KEYS)
    Key = models.IntegerField()
    Message = models.CharField(max_length=100)