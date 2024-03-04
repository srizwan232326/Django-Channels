from celery import shared_task
from .models import plcparameter , word_batch_read
import asyncio
import pymcprotocol
from asgiref.sync import sync_to_async
from time import time

class MyTask:
    @staticmethod
    def another_function():
        return "Return value from another function"

@shared_task(bind=True)
def print_test(self):
    for i in range(10):
        print(i)
    
    my_task_instance = MyTask()
    result_of_another_function = my_task_instance.another_function()
    print(result_of_another_function)
    return "Hello, World!"

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

    async def main(self):
        bit_start_address = 'L0'
        await self.connect()
        await asyncio.sleep(1)

        read_bits_l0_to_l100 = self.plcobj.batchread_bitunits(headdevice=bit_start_address, readsize=10)

        for i, value in enumerate(read_bits_l0_to_l100):
            print(f"L{i} Value --->", value)

        self.close_connection()

    def close_connection(self):
        self.plcobj.close()
        print("Connection closed")

@shared_task(bind=True)
def mplc_main_task(self, ip_addr, port, plctype, commtype):
    mplc = MPLC(ip_addr=ip_addr, port=port, plctype=plctype, commtype=commtype)
    asyncio.run(mplc.main())