from django.db import models
import time

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
        ('intzr', 'intzr'),
        ('string', 'string'),
        ('single-precision', 'single-precision'), 
        ('double-precision', 'double-precision')
    ])
    no_of_char = models.IntegerField(null=True)

class TriggerConfiguration(models.Model):
    tag = models.ForeignKey(device_tag_setting, on_delete=models.CASCADE)
    address = models.CharField(max_length=100 , null=True, blank=True)
    comment = models.CharField(max_length=100 , null=True, blank=True)

class Triggerloggers(models.Model):
    triggertag = models.ForeignKey(TriggerConfiguration, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, null=True, blank=True)

class datatrigger(models.Model):
    tag = models.ForeignKey(device_tag_setting, on_delete=models.CASCADE)
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

class RobotCycleDataHistory(models.Model):
    daytime = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    spare1 = models.CharField(max_length=100, null=True, blank=True)
    spare2 = models.CharField(max_length=100, null=True, blank=True)
    L_resin_Paint_cons = models.IntegerField(null=True, blank=True)
    L_hardener_Paint_cons = models.IntegerField(null=True, blank=True)
    L_ratio = models.IntegerField(null=True, blank=True)
    R_resin_Paint_cons = models.IntegerField(null=True, blank=True)
    R_hardener_Paint_cons = models.IntegerField(null=True, blank=True)
    R_ratio = models.IntegerField(null=True, blank=True)

#/////////////////////////////////////////TRACIBILITY///////////////////////////////////////////

class LoadingstationData(models.Model):
    created_at = models.DateTimeField()
    hanger_no = models.IntegerField(null=True)
    program_no = models.IntegerField(null=True)
    color_no = models.IntegerField(null=True)
    color_code = models.CharField(max_length=10, null=True)
    color_code_man = models.CharField(max_length=10, null=True)
    last_zone = models.IntegerField(null=True)
    live_status = models.IntegerField(null=True)
    category = models.CharField(max_length=10, null=True)
    
class part(models.Model):
    LoadingStation = models.ForeignKey(LoadingstationData, on_delete=models.CASCADE)
    ln_code = models.CharField(max_length=100, null=True, blank=True)
    production_id = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    warehouse_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)


class zonedata1(models.Model):
    LoadingStation = models.ForeignKey(LoadingstationData, on_delete=models.CASCADE)
    intime = models.CharField(max_length=100, null=True, blank=True)
    outtime = models.CharField(max_length=100, null=True, blank=True)
    pausetime = models.IntegerField(null=True, blank=True)

class zonedata2(models.Model):
    LoadingStation = models.ForeignKey(LoadingstationData, on_delete=models.CASCADE)
    intime = models.CharField(max_length=100, null=True, blank=True)
    degrease_circ_pump = models.BooleanField(null=True, blank=True)
    degrease_heat_pump = models.BooleanField(null=True, blank=True)
    buner = models.BooleanField(null=True, blank=True)
    deg_hot_water_diff_prs = models.IntegerField(null=True, blank=True)
    deg_circ_pump_prs = models.IntegerField(null= True ,blank=True)
    deg_circ_flow = models.IntegerField(null= True, blank=True)
    deg_tank_temp = models.IntegerField(null=True, blank=True)
    deg_tank_level = models.IntegerField(null=True, blank=True)



