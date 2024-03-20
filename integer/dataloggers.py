from asgiref.sync import sync_to_async  # Import sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import device_tag_setting, datatrigger
import asyncio

async def interval_logger(self, result):
    global initial_run
    if initial_run:
        initial_run = False
        print("interval_logger called")
        await asyncio.sleep(5) 
        print("after sleep in interval_logger")
        tag = 'D100'
        value = result.get(tag)
        if value is not None:
            try:
                await save_trigger_data_async(tag, value)
            except Exception as e:
                print(f"An error occurred while logging data: {e}")
        else:
            print("Tag address not found in the PLC data.")
        initial_run = True

async def save_trigger_data_async(tag, value):
    try:
        device_tag = await sync_to_async(device_tag_setting.objects.get)(address=tag)
        print("DeviceTagSetting found for tag:", tag, "value:", value)
        await sync_to_async(datatrigger.objects.create)(tag=device_tag, value=value)
    except ObjectDoesNotExist:
        print("DeviceTagSetting does not exist for tag:", tag)
    except Exception as e:
        print(f"An error occurred while saving trigger data: {e}")

def interval_logger_threaded(self, result):
    asyncio.run(interval_logger(self, result))

initial_run = True
