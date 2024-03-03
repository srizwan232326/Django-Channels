from celery import shared_task
from django.conf import settings
from .consumers import WSConsumer	
from celery import shared_task

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
