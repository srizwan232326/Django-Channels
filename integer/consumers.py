from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import pymcprotocol
from .views import *


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

    async def fetch_plc_data(self):
        bit_start_address = 'D100'
        read_bits_l0_to_l100 = self.plcobj.batchread_wordunits(headdevice=bit_start_address, readsize=10)
        result = {f"{bit_start_address}-{i}": value for i, value in enumerate(read_bits_l0_to_l100)}
        result = {f"D{100+i}": value for i, (key, value) in enumerate(result.items())}

        d100_value = result.get('D100', 0)

        if d100_value == 1:
            print("D100 is ON")
            if not hasattr(self, 'plc_data_saved') or not self.plc_data_saved:
                await save_plc_data_async(result.get('D101', 0), result.get('D102', 0), result.get('D103', 0), result.get('D104', 0), result.get('D105', 0))
                self.plc_data_saved = True 
        elif d100_value == 0:
            self.plc_data_saved = False
        return result
    def close_connection(self):
        self.plcobj.close()
        print("Connection closed")

class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        mplc = MPLC(ip_addr="192.169.4.30", port=8001, plctype="L", commtype="binary")
        await mplc.connect()
        while True:
            plc_data = await mplc.fetch_plc_data()
            print(plc_data)
            await self.send(text_data=json.dumps(plc_data))
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        pass 
