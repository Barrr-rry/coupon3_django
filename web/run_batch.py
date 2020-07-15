from run_init import *
from django.db import transaction
import json
import os
from PIL import Image

with transaction.atomic():
    queryset = StoreDiscount.objects.filter(description__icontains='活動網址')
    for el in queryset:
        desc = el.description
        print(el.description)
        desc = desc.replace('- 活動網址：', '【 活動網址 】：')
        el.description = desc
        el.save()
