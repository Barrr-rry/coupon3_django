from crawler import reids_wraper
from run_init import *

from log import logger
import traceback
from django.http import HttpResponse
import requests
import os

token = 'PAy6SmSfpfEI6nNN8K4cQKsUcjve4kxCWg03B49Tqt4'
DEBUG = os.environ.get('ENV') != 'prod'


def line_notify(msg):
    """
    line 通知功能
    """
    # 開發機 不需要通知 不然會收不完
    if DEBUG:
        return
    url = "https://notify-api.line.me/api/notify"

    headers = {
        "Authorization": "Bearer " + token
    }

    payload = {'message': msg}
    r = requests.post(url, headers=headers, params=payload)
    return r.status_code


# 把template or 其他 所有的cache 都清除掉 常用來部署的時候 把cache 清除掉
for key in reids_wraper.r.keys():
    reids_wraper.r.delete(key)
# 更新狀態成 正常
instance = ConfigSetting.objects.first()
if not instance:
    ConfigSetting.objects.create(
        in_maintenance=False
    )
else:
    instance.in_maintenance = False
    instance.save()

line_notify('部署完畢')
logger.info('部署完畢')
