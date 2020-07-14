from run_init import *
from django.db import transaction
import json
import os
from PIL import Image

desc = """【活動說明】：經政府公告，本網站可使用三倍券。

【活動時間】：2020/7/15 ~ 2020/12/31。

【活動網站】：https://3000.gov.tw/News.aspx?n=53&sms=9110 。"""
with transaction.atomic():
    queryset = StoreDiscount.objects.filter(picture__icontains='.webp')
    for el in queryset:
        img_path = os.path.join('media', el.picture)
        if not os.path.exists(img_path):
            print('not found pic:', el.picture)
            el.picture = None
            el.save()
        else:
            img_full_name = el.picture
            img_name = img_full_name.replace(f'.{img_full_name.split(".")[-1]}', '')  # 檔名稱
            output = img_name + ".jpeg"  # 輸出檔名稱
            im = Image.open(os.path.join('media', img_full_name))  # 讀入檔案
            im = im.convert("RGB")
            im.save(os.path.join('media', output), "JPEG", optimize=True, quality=70)  # 儲存
            img_full_path = os.path.join('media', img_full_name)
            el.picture = output
            el.save()
            # if os.path.exists(img_full_path):
            #     os.remove(img_full_path)

    queryset = StoreImage.objects.filter(picture__icontains='.webp')
    for el in queryset:
        img_path = os.path.join('media', el.picture)
        if not os.path.exists(img_path):
            print('not found pic:', el.picture)
            el.picture = None
            el.save()
        else:
            img_full_name = el.picture
            img_name = img_full_name.replace(f'.{img_full_name.split(".")[-1]}', '')  # 檔名稱
            output = img_name + ".jpeg"  # 輸出檔名稱
            im = Image.open(os.path.join('media', img_full_name))  # 讀入檔案
            im = im.convert("RGB")
            im.save(os.path.join('media', output), "JPEG", optimize=True, quality=70)  # 儲存
            img_full_path = os.path.join('media', img_full_name)
            el.picture = output
            el.save()
            # if os.path.exists(img_full_path):
            #     os.remove(img_full_path)
