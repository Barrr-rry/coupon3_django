import requests
from pyquery import PyQuery as pq
from PIL import Image
import os
from io import BytesIO
import json

"""
過去的爬蟲匯入資料 如果不需要就可以刪掉了
"""
url = 'https://3000.gov.tw/News.aspx?n=53&sms=9110&page=1&PageSize=200'
r = requests.get(url)
dom = pq(r.text)
ret = []
for el in dom('tbody > tr').items():
    website = el('a').attr('href')
    name = el('td').eq(2).text()
    desc = el('.p > p > span').text()

    img_name = None
    ret.append(dict(
        store_type_id=8,
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
                description="""活動說明：經政府公告，本網站可使用三倍券。

活動時間：2020/7/15 ~ 2020/12/31。

活動網站：https://3000.gov.tw/News.aspx?n=53&sms=9110 。"""
            )
        ]
    ))

with open('./other.json', 'w') as f:
    f.write(json.dumps(ret))
