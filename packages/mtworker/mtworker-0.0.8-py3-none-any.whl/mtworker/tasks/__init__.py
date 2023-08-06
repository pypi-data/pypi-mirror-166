from celery import shared_task,chord, group, signature, uuid
import requests
import logging
import time
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from .demoTask import *
from .getUrlBody import *
from .bot_status import *
from .helloworld import *

# 运行最终结果同一提交到此网址
result_api = "https://mtxcms-d.csrep.top/mtxcms/taskresult/"
@shared_task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y

@shared_task
def mul(x, y):
    logger.info(f'乘法任务 {x} / {y}')
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def mtworker_debug(x):    
    body = {
        "task":"mtworker_debug",
        "data": x,
    }
    logger.info(f'运行结果同一提交到 {result_api},\n数据: {body}')
    response = requests.post(result_api,data=body)
    logger.info(f"提交数据结果: {response}")
    return x

@shared_task
def debug_info():    
    return ""


# @shared_task
# def count_widgets():
#     return Widget.objects.count()


# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()






