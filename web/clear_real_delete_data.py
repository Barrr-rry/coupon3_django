import json
from run_init import *
from django.db import transaction, router
from log import logger

# 如果store 被刪掉 其他的img dis 等 都要一起被真的刪掉
with transaction.atomic():
    queryset = Store.original_objects.filter(deleted_status=True)
    for el in queryset:
        for img in el.storeimage.all():
            img.real_delete()
        for dis in el.storediscount.all():
            dis.real_delete()
        el.real_delete()
