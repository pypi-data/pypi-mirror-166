#!/usr/bin/env python3


#
# 启动方式：celery -A mtworker worker --loglevel=INFO
#          celery -A mtworker worker --loglevel=INFO -Q mtworker
# 
import os
from celery import Celery
from stem.control import Controller
import stem
import stem.process
from stem.util import term
import requests
from celery import shared_task,chord, group, signature, uuid
from celery.signals import (
    after_setup_task_logger,
    task_success,
    task_prerun,
    task_postrun,
    celeryd_after_setup,
    celeryd_init,
)
from celery.utils.log import get_task_logger
from .tasks import add
from .taskUtil import load_init_config_from_api
import logging
logger = get_task_logger(__name__)

# CELERY_BROKER_STR="pyamqp://admin:feihuo321@rabbitmq//"
# CELERY_REDIS_STR="redis://:feihuo321@redis"

MTWORKER_BACKENDAPI= os.environ.get("MTWORKER_BACKENDAPI")
# backendApi="https://mtxcms-d.csrep.top/mtxcms/taskresult/"



def create_celery_app():
    # 从django setting 中的配置信息，
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtxcms.settings.base') 
    
    celery_app_name = "mtworker"
    app = Celery(celery_app_name, 
        # broker=CELERY_BROKER_STR, 
        # backend=CELERY_REDIS_STR,
        include=['mtworker.tasks'],
        )
    # init_config_data = load_init_config_from_api(app)
    # djSetting = os.environ.get("DJANGO_SETTINGS_MODULE")
    if os.environ.get("DJANGO_SETTINGS_MODULE"):
        print(f"当前存在django环境。从django setting 加载并初始化celery。")
        # namespace="CELERY"的含义是：变量前缀CELERY_ 的才是别为CELERY配置。
        app.config_from_object('django.conf:settings', namespace='CELERY')
        
    elif MTWORKER_BACKENDAPI:
        print(f"从后端api加载celery初始化设置")
        response = requests.get(MTWORKER_BACKENDAPI+"?action=celery_config")
        config  = response.json()
        print(f"配置数据{config}")
    else:
        # 可以直接更新配置。
        app.config.update({
            "timezone":"UTC",
            # "broker_url": os.environ.get("CELERY_BROKER_URL"),
            # "result_backend": os.environ.get("CELERY_RESULT_BACKEND"),
        })
    
    # app.conf.timezone = 'UTC'
    app.autodiscover_tasks()
    
    print(f"当前celery app 配置信息:\n{app.config}")
    return app

app = create_celery_app()

    
# app.conf.task_routes = {
#     'mtx_cloud.tasks.*': {'queue': 'mtx_cloud'},
#     'mtworker.tasks.*': {'queue': 'mtworker'}
# }

@after_setup_task_logger.connect()
def setup_task_logger(logger, *args, **kwargs):
    print(f"[after_setup_task_logger]")
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s [%(lineno)d]')
    # 增加文件日志。
    # FileHandler
    fh = logging.FileHandler('.mtworker.celery.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # 修改日志级别，10为最详细，40，最小。
    logger.level=10
    
    # StreamHandler[这个日志方式还不太明白，难道是控制台的日志输出？不是自带了的吗？]
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
        
    # SysLogHandler（远程日志？）
    # slh = logging.handlers.SysLogHandler(address=('logsN.papertrailapp.com', '...'))
    # slh.setFormatter(formatter)
    # logger.addHandler(slh)
    
    # 日志格式。
    # for handler in logger.handlers:
    #     logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s [%(lineno)d]')
    #     # handler.setFormatter(TaskFormatter('%(asctime)s - %(task_id)s - %(task_name)s - %(name)s - %(levelname)s - %(message)s'))

@task_success.connect()
def task_succeeded(result, sender=None, task_id=None, task=None, **kwargs):
    if MTWORKER_BACKENDAPI:
        print("任务完成,结果: result: {result}, task_id:{task_id}, task: {task}")
        print("sender: " + str(sender))
        print("request_id:" + sender.request.id)
        
        postData = {
            "result": result
        }
        response = requests.post(MTWORKER_BACKENDAPI, data=postData)
        if response.status_code != 200:
            logger.error(f"提交数据api, 不成功, status_code:{response.status_code}")
            
        logger.info(f"结果已经提交到 backendApi")
    
    

@task_prerun.connect(sender=add)
def task_prerun_notifier(sender=None, **kwargs):
    print("From task_prerun_notifier ==> Running just before add() executes")

@task_postrun.connect(sender=add)
def task_postrun_notifier(sender=None, **kwargs):
    print("From task_postrun_notifier ==> Ok, done!")

@task_success.connect(sender=add)
def task_success_notifier(sender=None, **kwargs):
    print("From task_success_notifier ==> Task run successfully!")


# ######################################################################
# 定时任务
# 需要预先启动beat 由beat来发送定时任务到worker
# `celery -A mtxcms beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`
# 需要注意的是：DatabaseScheduler 这个调度器，应该是以数据库的数据为准。
# 而下面的配置，在程序初始化时，会自动写入数据库。当然也可以直接在django admin PERIODIC TASKS 这里添加对应的计划任务， 会自动生效。
# app.conf.beat_schedule = {
#     # 每分钟执行一次。
#     # 'send-report-every-single-minute': {
#     #     'task': 'mtxcms.celery.debug_task',
#     #     'schedule': crontab(),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
#     # },
#     'add-every-30-seconds': { #
#         'task': 'demoapp.tasks.getUrlBody',  #任务标识
#         'schedule': 30.0,     #每30秒
#         'args': ("http://www.baidu.com/",)      #任务参数
#     },
# }

@app.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    # 似乎没生效。
    print(f"[on_after_configure]")
    # 就绪后，可以使用这个方式配置定时任务。
    # 而具体的配置数据，可以先从backend api，这里获取相关的配置数据。
    logger.info("[celery on_after_configure]")
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     debug_task.s('Happy Mondays!'),
    # )
    
@celeryd_after_setup.connect
def on_celeryd_after_setup(sender, instance, **kwargs):
    print(f"[on_celeryd_after_setup]")
    # queue_name = '{0}.dq'.format(sender)  # sender is the nodename of the worker
    # instance.app.amqp.queues.select_add(queue_name)
    
    
@celeryd_init.connect(sender='worker12@example.com')
def configure_worker12(conf=None, **kwargs):
    print(f"[celeryd_init]")
    conf.task_default_rate_limit = '10/m'
    
@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    # if sender in ('worker1@example.com', 'worker2@example.com'):
    #     conf.task_default_rate_limit = '10/m'
    # if sender == 'worker3@example.com':
    #     conf.worker_prefetch_multiplier = 0
    pass
        
def start_worker():
    # app = current_app._get_current_object()
    app = create_celery_app()
    app.autodiscover_tasks()
    worker = app.Worker(
        include=['mtworker.tasks'],
        # on_start=aa
    )
    for task in worker.app.tasks:
        logger.info(f"任务：{task}")
    logger.info("mtworker 就绪")
    worker.start()
    
def main():
    # start_worker()
    app.start()

if __name__ == '__main__':
    main()
