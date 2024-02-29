from django.db import models

class plc(models.Model):
    zone_a = models.IntegerField(null=True)
    zone_b = models.IntegerField(null=True)
    zone_c = models.IntegerField(null=True)
    zone_d = models.IntegerField(null=True)
    zone_e = models.IntegerField(null=True)

