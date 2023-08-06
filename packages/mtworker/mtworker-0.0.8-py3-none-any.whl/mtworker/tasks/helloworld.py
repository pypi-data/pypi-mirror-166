from celery import shared_task,chord, group, signature, uuid
import requests
import logging
import time
from ..taskUtil import help1
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@shared_task
def helloworld(hello="hello1", world="word1"):
    return {
        "hello": hello,
        "world":world
}  
    
    