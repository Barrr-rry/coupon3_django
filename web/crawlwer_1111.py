"""
抓取task https://bitbucket.org/ConquerTW/coupon3_django/issues/203/1111

"""
import requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin
import json

# 抓取target_urls

# search_urls = """
# https://marketing.1111.com.tw/uwhere/Search?Type=1684
# https://marketing.1111.com.tw/uwhere/Search?Type=1685
# https://marketing.1111.com.tw/uwhere/Search?Type=1687
# https://marketing.1111.com.tw/uwhere/Search?Type=1689
# https://marketing.1111.com.tw/uwhere/Search?Type=1686
# """
# search_urls = search_urls.split()
# target_urls = []
# for search_url in search_urls:
#     page = 1
#     while True:
#         url = f'{search_url}&page={page}'
#         print(url)
#         host_url = 'https://marketing.1111.com.tw'
#         r = requests.get(url)
#         doc = r.text
#         dom = pq(doc)
#         # 沒有資料
#         if not len(dom('.media-box-text > a')):
#             break
#         for el in dom('.media-box-text > a').items():
#             target_url = urljoin(host_url, el.attr('href'))
#             target_urls.append(target_url)
#         page += 1
#
# with open('./1111_urls.json', 'w') as f:
#     f.write(json.dumps(target_urls))
url  = 'https://trade.1111.com.tw/ProductImg/Upload/Marketing/A_plus/uwhere/AD/25226/%E9%AC%BC%E7%82%8A071.jpg'

r = requests.get(url)
if r.status_code == 200:
    with open("/Users/apple/Desktop/sample.jpg", 'wb') as f:
        f.write(r.content)

# target_urls = []
# with open('./1111_urls.json') as f:
#     target_urls = json.loads(f.read())
print()
