import asyncio
from .models import device_tag_setting, datatrigger
from asgiref.sync import sync_to_async

class LoggingMicroservice:
    def __init__(self):
        self.logging_task_running = False

    async def start_logging(self, result):
        if not self.logging_task_running:
            self.logging_task_running = True
            await self.logging_loop(result)

    async def logging_loop(self, result):
        while self.logging_task_running:
            await self.data_logging_on_interval(result)

    async def data_logging_on_interval(self, plc_address_and_value):
        if plc_address_and_value is None:
            print("Error: PLC address and value data is None.")
            self.logging_task_running = False
            return

        address = 'D100'
        tag_address = plc_address_and_value.get(address)

        if tag_address is not None:
            try:
                await self.save_trigger_data_async(address, tag_address)
            except Exception as e:
                print(f"An error occurred while logging data: {e}")
        else:
            print("Tag address not found in the PLC data.")
            self.logging_task_running = False

    async def save_trigger_data_async(self, tag, value):
        try:
            device_tag = await sync_to_async(device_tag_setting.objects.get)(address=tag)
            await sync_to_async(datatrigger.objects.create)(
                tag=device_tag,
                value=value
            )
        except device_tag_setting.DoesNotExist:
            print("device_tag_setting does not exist for tag:", tag)
        except Exception as e:
            print(f"An error occurred while saving trigger data: {e}")
        finally:
            await asyncio.sleep(10)
            self.logging_task_running = False
