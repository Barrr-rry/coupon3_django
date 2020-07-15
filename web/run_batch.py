from run_init import *
from django.db import transaction
import json
import os
from PIL import Image
import re

"""
【 活動內容 】：
【 活動期間 】：2020/7/15 ~ 2020/12/31
【 活動說明 】：
＊（請輸入活動說明，記得刪除本行）
＊（請輸入活動說明，記得刪除本行）
（1）
（2）
（3）
＊（請輸入活動說明，記得刪除本行）
（1）
（2）
（3）
【 活動網址 】：
"""

with transaction.atomic():
    queryset = StoreDiscount.objects.filter(description__icontains='- ')
    for el in queryset:
        desc = el.description
        print(el.store.id)
        # print(desc)
        for line in desc.split('\n'):
            line = line.strip('\r')
            if '-' in line:
                new_line = line.replace('- ', '＊').strip()
                desc = desc.replace(line, new_line)
            if re.findall('\(\d+?\)', line):
                new_line = line.replace('(', '（').replace(')', '）').strip()
                desc = desc.replace(line, new_line)
                continue
        # print('@@@@' * 20)
        # print(desc)
        # print('-' * 20)
        el.description = desc
        el.save()
