from celery import shared_task
import asyncio
import pymcprotocol
import json
from .models import datalogger , device_tag_setting
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from time import sleep
from .views import *
from integer.dataloggers import *
class MPLC:
    def __init__(self, ip_addr, port, plctype, commtype):
        self.ip_addr = ip_addr
        self.port = port
        self.plcobj = pymcprotocol.Type3E(plctype=plctype)
        self.plcobj.setaccessopt(commtype=commtype)

    async def connect(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.plcobj.connect, self.ip_addr, self.port)
        print("Connected to PLC")

    def close_connection(self):
            self.plcobj.close()
            print("Connection closed")
            
    @database_sync_to_async
    def get_plc_tags(self):
        connected_ip = self.ip_addr
        return [{'address': record.address, 'data_type': record.data_type , 'readsize' : record.no_of_char} for record in device_tag_setting.objects.filter(plc__plc_ip=connected_ip)]
    
    async def main(self):
        if not self.plcobj._is_connected:
            await self.connect()
        else:
            print("Already connected to PLC")
            addresses = await self.get_plc_tags()
            sleep(0)
            result = {} 
            for address in addresses:
                plc_address = str(address['address'])
                data_type = str(address['data_type'])
                readsize = int(address['readsize']) if address.get('readsize') else 1

                if data_type == 'int':
                    intread = self.plcobj.batchread_wordunits(headdevice=str(plc_address), readsize=readsize)
                    result[plc_address] = intread[0]


                elif data_type == 'dint':
                    dint_read = self.plcobj.randomread(word_devices=[], dword_devices=[plc_address])
                    result[plc_address] = dint_read[1][0]


                elif data_type == 'string':
                    string_read = self.plcobj.batchread_wordunits(headdevice=str(plc_address), readsize=int(round(readsize/2)))
                    decimal_values = string_read
                    string_result = ''
                    for decimal_value in decimal_values:
                        hex_representation = hex(decimal_value)[2:]
                        hex_representation = '0' + hex_representation if len(hex_representation) % 2 != 0 else hex_representation
                        ascii_characters = [bytes.fromhex(hex_representation[i:i+2]).decode('utf-8') for i in range(0, len(hex_representation), 2)]
                        string_result += ''.join(ascii_characters[::-1])
                    result[plc_address] = string_result

            if isinstance(result,dict):
                    result_value = result.get('D100')
                    if result_value==1 :
                        if not hasattr(self, 'plc_data_saved') or not self.plc_data_saved:
                            await save_plc_data_async(result.get('D101', 0 ), result.get('D102',0), result.get('D104',0))
                            tag_settings = await self.get_plc_tags()
                            print(tag_settings)
                            address_mapping = {tag['address']: result.get(tag['address'], 0) for tag in tag_settings}
                            address_mapping.pop('D100', None)
                            print("Original address_mapping:", address_mapping)
                            test = await save_plc_data_async(*list(address_mapping.values()))
   
                            print(test)
                            await save_plc_data_async(list(address_mapping.values()))                              
                            await self.wordWriteBatch('D100', [2])
                            self.plc_data_saved = False
                    elif result_value == 0:
                        self.plc_data_saved = False
            else:
                print("Invalid result type. Expected a dictionary.")

            return result
    #//////////////////////////////////CYCLIC DATA LOGGING////////////////////////////////////////


        

    #//////////////////////////////////CYCLIC DATA LOGGING////////////////////////////////////////
    async def wordWriteBatch(self, device, value_batch_list):
        self.plcobj.batchwrite_wordunits(headdevice=device, values=value_batch_list)
        return "Write operation successful"


initail_run = True
if initail_run:
    class MPLCMainTask:
        def __init__(self, plc_make, plc_series, plc_ip, plc_port, plc_communication_type):
            self.mplc = MPLC(ip_addr=plc_ip, port=plc_port, plctype=plc_series, commtype=plc_communication_type)

        def run(self):
            try:
                while True:
                    result= asyncio.run(self.mplc.main())
                    print('result is',result)
                    initail_run = False
                    if result:
                        logging_microservice = LoggingMicroservice()
                        asyncio.run(logging_microservice.start_logging(result))
            except Exception as e:
                print(e)
                initail_run = True
            finally:
                self.mplc.close_connection()
                print("PLC connection completed")

@shared_task(bind=True)
def mplc_main_task(self):
    plc_info = datalogger.objects.first()
    print(plc_info)
    if plc_info:
        mplc_task = MPLCMainTask(
            plc_make=plc_info.Plc_make,
            plc_series=plc_info.plc_series,
            plc_ip=plc_info.plc_ip,
            plc_port=plc_info.plc_port,
            plc_communication_type=plc_info.plc_communication_type
        )
        mplc_task.run()