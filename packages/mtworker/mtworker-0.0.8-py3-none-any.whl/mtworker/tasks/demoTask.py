from celery import shared_task,chord, group, signature, uuid
import requests
import logging
import time
from ..taskUtil import help1
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@shared_task
def demo(url):
    value1 = help1()
    return str(f"demo task {value1}, {url} ")
