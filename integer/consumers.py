from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import pymcprotocol
from .views import *
from .models import plcparameter , word_batch_read
from channels.db import database_sync_to_async

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
    
    @database_sync_to_async
    def get_plc_tags(self):
        return word_batch_read.objects.get()

    async def fetch_plc_data(self):
        address = await self.get_plc_tags()
        bit_start_address = address.startaddress
        read_size = int(address.readsize)
        read_bits_l0_to_l100 = self.plcobj.batchread_wordunits(headdevice=str(bit_start_address), readsize=read_size)
        result = {f"{bit_start_address[:-1]}{i}": value for i, value in enumerate(read_bits_l0_to_l100)}
        d100_value = result.get('D100', 0)

        if d100_value == 1:
            print("D100 is ON")
            if not hasattr(self, 'plc_data_saved') or not self.plc_data_saved:
                await save_plc_data_async(result.get('D101', 0), result.get('D102', 0), result.get('D103', 0), result.get('D104', 0), result.get('D105', 0))
                plc_write = await self.wordWriteBatch('D100', [2])
                print(plc_write)
                self.plc_data_saved = True 
        elif d100_value == 0:
            self.plc_data_saved = False
        return result
    
    async def wordWriteBatch(self, device, value_batch_list):
        self.plcobj.batchwrite_wordunits(headdevice=device, values=value_batch_list)
        return "Write operation successful"  # or any other meaningful return value

        
    def close_connection(self):
        self.plcobj.close()
        print("Connection closed")

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        plc_params = await self.get_plc_params()
        mplc = MPLC(ip_addr=plc_params.plc_ip,port=plc_params.plc_port,plctype=plc_params.plc_series,commtype=plc_params.plc_communication_type)
        await mplc.connect()
        while True:
            plc_data = await mplc.fetch_plc_data()
            print(plc_data)
            await self.send(text_data=json.dumps(plc_data))
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_plc_params(self):
        return plcparameter.objects.first()
    
