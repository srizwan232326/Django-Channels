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


#///////////////////////////////////////////data logger///////////////////////////////////////////


class datalogger(models.Model):
    Plc_make = models.CharField(max_length=100, choices=[('Mitsubishi', 'Mitsubishi')])
    plc_series = models.CharField(max_length=100, choices=[('Q', 'Q'), ('L', 'L'), ('QnA', 'QnA'), ('iQ-L', 'iQ-L'), ('iQ-R', 'iQ-R')])
    plc_ip = models.CharField(max_length=100)
    plc_port = models.IntegerField()
    plc_communication_type = models.CharField(max_length=100, choices=[('binary', 'binary'), ('ascii', 'ascii')])

class device_tag_setting(models.Model):
    id = models.AutoField(primary_key=True)
    plc = models.ForeignKey(datalogger, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100, choices=[
        ('bit', 'bit'), 
        ('int', 'int'), 
        ('dint', 'dint'),
        ('string', 'string'),
        ('single-precision', 'single-precision'), 
        ('double-precision', 'double-precision')
    ])
    time = models.CharField(max_length=100, choices=[
        ('1sec', '1sec'), 
        ('5sec', '5sec'), 
        ('60sec', '60sec'), 
        ('10min', '10min')
    ])
    no_of_char = models.IntegerField(null=True)


class datatrigger(models.Model):
    tag = models.ForeignKey(device_tag_setting, on_delete=models.CASCADE)
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class datahistory(models.Model):
    count = models.IntegerField(null=True)
    doublecount = models.IntegerField(null=True)
    char = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


