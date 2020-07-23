import requests
from pyquery import PyQuery as pq
from PIL import Image
import os
from io import BytesIO
import json

"""
過去的爬蟲匯入資料 如果不需要就可以刪掉了
"""
url = 'https://3000.gov.tw/News_Photo.aspx?n=24&sms=9054'
r = requests.get(url)
dom = pq(r.text)
ret = []
for el in dom('a.div').items():
    website = el.attr('href')
    name = el('.figcaption > span').text()
    desc = el('.p > p > span').text()
    img_url = el('span > img').attr('src')
    r = requests.get(img_url)
    img_full_name = img_url.split('/')[-1]

    img_name = img_full_name.replace(f".{img_full_name.split('.')[-1]}", '.webp')
    f = BytesIO()
    f.write(r.content)
    img = Image.open(f)
    img.save(os.path.join('media', img_name))
    ret.append(dict(
        store_type_id=7,
        status=0,
        search_status=2,
        name=name,
        website=website,
        # store image
        store_image_picture=img_name,
        store_discount=[
            dict(
                discount_type_id=14,
                name='本行卡可使用三倍券回饋',
                description="""活動說明：累計消費滿 3,000 元，帳單直接扣 2,000 元。

活動時間：2020/7/15 ~ 2020/12/31。

活動辦法：2020/7/01 起到銀行網站綁定信用卡，收到通知，最晚下個月帳單額度就會看到回饋！

活動網站：https://3000.gov.tw/News_Photo.aspx?n=24&sms=9054 。
                """
            ),
            dict(
                discount_type_id=14,
                name=None,
                description=desc,
            )
        ]
    ))

print(ret)
with open('./credit.json', 'w') as f:
    f.write(json.dumps(ret))
