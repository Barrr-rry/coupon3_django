from run_init import *
from django.db import transaction
import json

desc = """【活動說明】：經政府公告，本網站可使用三倍券。

【活動時間】：2020/7/15 ~ 2020/12/31。

【活動網站】：https://3000.gov.tw/News.aspx?n=53&sms=9110 。"""
with transaction.atomic():
    queryset = Store.objects.filter(id__gte=12579, id__lte=12749)
    queryset.delete()
    queryset = Store.objects.filter(id__gte=12370, id__lte=12540)
    for el in queryset:
        dis = el.storediscount.first()
        dis.description = desc
        dis.save()
