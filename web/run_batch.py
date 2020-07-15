from run_init import *
from django.db import transaction
import json
import os
from PIL import Image

"""
如果 google place 有跑到資料的 先把 status改審核通過
"""
with transaction.atomic():
    activity = Activity.objects.get(pk=27)
    for el in activity.store.all():
        if el.google_status == 1:
            print(el.id)
            el.status = 1
            el.save()
