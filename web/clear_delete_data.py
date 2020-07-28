import json
from run_init import *
from django.db import transaction, router
from log import logger

# 如果store 被刪掉 其他的img dis 等 都要一起被刪掉
for el in Store.objects.raw('SELECT id FROM api_store'):
    print(el.location)
    # for img in el.storeimage.all():
    #     img.deleted_status = True
    #     img.save()
    # for dis in el.storediscount.all():
    #     dis.deleted_status = True
    #     dis.save()
