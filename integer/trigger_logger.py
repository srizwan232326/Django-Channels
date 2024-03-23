from .views import *
from integer.dataloggers import *
from .models import  LoadingStation , part , zonedata1 , zonedata2
from asyncio import sleep

async def triggerlogger(result, self):
    if isinstance(result, dict):
        tag_settings = await self.get_trigger_tags()
        print("tag_settings:", tag_settings)
        result_value = {trigger['trigger_tag']: result.get(trigger['trigger_tag']) for trigger in tag_settings}
        
        if any(value == 1 for value in result_value.values()):
            if not getattr(self, 'plc_data_saved', False):
                address_mapping = {tag['log_tag']: result.get(tag['log_tag'], 0) for tag in tag_settings}
                print("address_mapping:", address_mapping)
                test = await save_plc_data_async(*list(address_mapping.values()))
                await save_plc_data_async(list(address_mapping.values()))

                for trigger_tag, value in result_value.items():
                    if value == 1:
                        tag_start_add_dec = int(trigger_tag[2:])
                        if trigger_tag.startswith('ZR'):
                            tag_start_add_hex = 'ZR' + hex(tag_start_add_dec)[2:]
                            await self.wordWriteBatch(tag_start_add_hex, [2])
                        else:
                            await self.wordWriteBatch(trigger_tag, data=[2])               
                self.plc_data_saved = True 
        else:
            self.plc_data_saved = False
    else:
        print("Invalid result type. Expected a dictionary.")

async def traceability_logger(result, self):
    if isinstance(result, dict):
        trigger_tag = 'D100'
        hanger_tag = 'D101'
        zone_no_tag = 'D102'
        live_status_tag = 'D103'
        
        value = result.get(trigger_tag)
        hanger_no = result.get(hanger_tag)
        zone_no = result.get(zone_no_tag)
        live_status = result.get(live_status_tag)
        
        if value == 1:
            if isinstance(zone_no, int): 
                if zone_no == 1:
                    query = LoadingStation.objects.filter(hanger_number=hanger_no, live_status=live_status)
                    if query.exists():
                        if not getattr(self, 'plc_data_saved', False):
                            try:
                                zonedata1.objects.create(
                                    LoadingStation=query.first(),
                                    intime=result.get('D104'),
                                    outtime=result.get('D105'),
                                    pausetime=result.get('D106')
                                )
                                setattr(self, 'plc_data_saved', True) 
                            except Exception as e:
                                print(f"An error occurred while saving zonedata1: {e}")
                    else:
                        print("Loading station does not exist for hanger number:", hanger_no)
                
                elif zone_no == 2:
                    query = LoadingStation.objects.filter(hanger_number=hanger_no, live_status=live_status)
                    if query.exists():
                        if not getattr(self, 'plc_data_saved', False):
                            try:
                                zonedata2.objects.create(
                                    LoadingStation=query.first(),
                                    intime=result.get('D110'),
                                    degrease_circ_pump=result.get('D111'),
                                    degrease_heat_pump=result.get('D112'),
                                    buner=result.get('D113'),
                                    deg_hot_water_diff_prs=result.get('D114'),
                                    deg_circ_pump_prs=result.get('D115'),
                                    deg_circ_flow=result.get('D116'),
                                    deg_tank_temp=result.get('D117'),
                                    deg_tank_level=result.get('D118')
                                )
                                setattr(self, 'plc_data_saved', True) 
                            except Exception as e:
                                print(f"An error occurred while saving zonedata2: {e}")
                    else:
                        print("Loading station does not exist for hanger number:", hanger_no)
                else:
                    print("Invalid zone number:", zone_no)
            else:
                print("Zone number is not an integer.")
        else:
            print("Trigger tag value is not 1.")
    else:
        print("Result is not a dictionary.")

