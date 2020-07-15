from run_init import *
from django.db import transaction
import json
import os
from PIL import Image

"""
12370兩廳院～12540嘉明湖國家步道山屋

12579兩廳院～12749嘉明湖國家步道山屋

資料都重複了，請刪除一組

‌

剩餘一組資料改成：

原有之discount 敘述改成 （看是否 discount 改成同一筆）

【活動說明】：經政府公告，本網站可使用三倍券。

【活動時間】：2020/7/15 ~ 2020/12/31。

【活動網站】：https://3000.gov.tw/News.aspx?n=53&sms=9110 。

store_type 都改成電商

然後地理資訊都清空

status = 1
"""
store_type = StoreType.objects.filter(name='電商').first()
with transaction.atomic():
    queryset = Store.objects.filter(id__gte=12370, id__lte=12540)
    for el in queryset:
        el.status = 1
        el.store_type = store_type
        el.save()
