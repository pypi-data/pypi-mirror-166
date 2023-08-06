from celery import shared_task,chord, group, signature, uuid
import requests
import logging
import time
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def getUrlBody(url):
    print(f"任务[mtworker]getUrlBody,启动, 参数: url={url}")
    res = requests.get(url)
    print("任务getUrlBody,完成")
    return str(res.text)