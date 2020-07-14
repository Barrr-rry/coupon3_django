from run_init import *
from django.db import transaction
import json

desc = """【活動說明】：經政府公告，本網站可使用三倍券。

【活動時間】：2020/7/15 ~ 2020/12/31。

【活動網站】：https://3000.gov.tw/News.aspx?n=53&sms=9110 。"""
with transaction.atomic():
    queryset = StoreDiscount.objects.all()
    for el in queryset:
        if el.picture and len(el.picture) == 1:
            el.picture = None
            el.save()
        store = Store.objects.filter(id=el.store_id)
        if not store:
            print(f'remove dis id: {el.id} store id: {el.store_id}')
            el.delete()

    queryset = StoreImage.objects.all()
    for el in queryset:
        if el.picture and len(el.picture) == 1:
            el.picture = None
            el.save()
        store = Store.objects.filter(id=el.store_id)
        if not store:
            print(f'remove dis id: {el.id} store id: {el.store_id}')
            el.delete()
