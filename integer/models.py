from django.db import models

class plc(models.Model):
    zone_a = models.IntegerField(null=True)
    zone_b = models.IntegerField(null=True)
    zone_c = models.IntegerField(null=True)
    zone_d = models.IntegerField(null=True)
    zone_e = models.IntegerField(null=True)


class plcparameter(models.Model):
    Plc_make = models.CharField(max_length=100, choices=[('Mitsubishi', 'Mitsubishi')])
    plc_series = models.CharField(max_length=100, choices=[('Q', 'Q'), ('L', 'L'), ('QnA', 'QnA'), ('iQ-L', 'iQ-L'), ('iQ-R', 'iQ-R')])
    plc_ip = models.CharField(max_length=100)
    plc_port = models.IntegerField()
    plc_communication_type = models.CharField(max_length=100, choices=[('binary', 'binary'), ('ascii', 'ascii')])


class word_batch_read(models.Model):
    startaddress = models.CharField(max_length=100)
    readsize = models.IntegerField()


class LoadingStation(models.Model):
    hanger_number = models.IntegerField()
    live_status = models.IntegerField()
    zone_number = models.IntegerField()

class Zonedata(models.Model): 
    loading_station = models.ForeignKey('LoadingStation', on_delete=models.CASCADE)
    loading_zone1 = models.JSONField(null=True)
    degrease_zone2 = models.JSONField(null=True)

