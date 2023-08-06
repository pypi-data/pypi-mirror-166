from demoapp.models import Widget
from celery import shared_task,chord, group, signature, uuid
import requests
import logging
logger = logging.getLogger(__name__)
@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return Widget.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = Widget.objects.get(id=widget_id)
    w.name = name
    w.save()


@shared_task
def getUrlBody(url):
    print(f"任务[mtworker]getUrlBody,启动, 参数: url={url}")
    res = requests.get(url)
    print("任务getUrlBody,完成")
    return str(res.text)
