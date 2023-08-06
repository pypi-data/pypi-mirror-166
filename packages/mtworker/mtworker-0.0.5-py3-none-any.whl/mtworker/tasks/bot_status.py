from celery import shared_task,chord, group, signature, uuid
import requests
import logging
import time
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@shared_task(queue='mtworker')
def bot_status(**kwargs):
    """最终"""
    
    logger.info(f"bot_status_worker, kwargs: {kwargs}")
    
    try:
        logger.info(f"task: bot_status: kargs : {kwargs}")
        botId = kwargs.get("id")
        # bot = Bot.objects.get(pk=botId)
        # logger.info(f"准备检测 bot: {bot}")
        logger.info(f"TODO: [bot_status_worker],做真实的bot状态检测")
        
        inspect_result = {
            "online": True
        }
        
        time.sleep(3)
        # BotInspect.objects.create(ok=True, bot=bot)
        logger.info(f"返回值{inspect_result}")
        return str(inspect_result)
        

    except Exception as e:
        return {"success": False, "errorMessage": str(e)}