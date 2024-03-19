from .views import *
from integer.dataloggers import *
from .models import datalogger, device_tag_setting

async def triggerlogger(result, self):
    if isinstance(result, dict):
        tag_settings = await self.get_trigger_tags()
        print('i am test',tag_settings)
        result_value = {trigger['trigger_tag']: result.get(trigger['trigger_tag'], 0) for trigger in tag_settings}
        
        if any(value == 1 for value in result_value.values()):
            if not getattr(self, 'plc_data_saved', False):
                address_mapping = {tag['log_tag']: result.get(tag['log_tag'], 0) for tag in tag_settings}
                print("address_mapping:", address_mapping)
                test = await save_plc_data_async(*list(address_mapping.values()))
                await save_plc_data_async(list(address_mapping.values()))
                
                for trigger_tag, value in result_value.items():
                    if value == 1:
                        await self.wordWriteBatch(trigger_tag, [2])
                
                self.plc_data_saved = True  
            
        else:
            self.plc_data_saved = False
    else:
        print("Invalid result type. Expected a dictionary.")




