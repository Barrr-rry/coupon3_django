"""
抓取task https://bitbucket.org/ConquerTW/coupon3_django/issues/203/1111

"""
import requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin
import json
from google import find_place_id, get_place_info, get_photo


# 抓取target_urls


def save_urls():
    search_urls = """
    https://marketing.1111.com.tw/uwhere/Search?Type=1684
    https://marketing.1111.com.tw/uwhere/Search?Type=1685
    https://marketing.1111.com.tw/uwhere/Search?Type=1687
    https://marketing.1111.com.tw/uwhere/Search?Type=1689
    https://marketing.1111.com.tw/uwhere/Search?Type=1686
    """
    search_urls = search_urls.split()
    target_urls = []
    for search_url in search_urls:
        page = 1
        while True:
            url = f'{search_url}&page={page}'
            print(url)
            host_url = 'https://marketing.1111.com.tw'
            r = requests.get(url)
            doc = r.text
            dom = pq(doc)
            # 沒有資料
            if not len(dom('.media-box-text > a')):
                break
            for el in dom('.media-box-text > a').items():
                target_url = urljoin(host_url, el.attr('href'))
                target_urls.append(target_url)
            page += 1

    with open('./1111_urls.json', 'w') as f:
        f.write(json.dumps(target_urls))


def save_img(url):
    r = requests.get(url)
    if r.status_code == 200:
        file_name = url.split('/')[-1]
        with open(f"/media/{file_name}", 'wb') as f:
            f.write(r.content)
        return file_name


def crawlwer_1111():
    target_urls = []
    with open('./1111_urls.json') as f:
        target_urls = json.loads(f.read())
    retttt = []
    for target_url in target_urls:
        r = requests.get(target_url)
        doc = r.text
        dom = pq(doc)
        img = dom('[property="og:image"]').attr.content
        img = f'http:{img}'
        img = save_img(img)
        store_type = 9
        title = dom('html > head > title').text()
        ret = {'美食饗宴': 1, '旅遊住宿': 13, '居家生活': 5, '休閒娛樂': 6, '百貨量販': 8}
        for rett in ret:
            if rett in title:
                store_type = ret[rett]
        main_name = dom('#wrapper > div > div > div > div > div > div > div').eq(1).text()
        discount_name = dom('h1').text()
        discount = dom('#wrapper > div > div > div > div > div > div > div').eq(2)
        discount.remove('h1')
        discount_1 = discount.text()
        discount_2 = ''
        for el in dom('.Article_Content > p').items():
            if el.text():
                discount_2 += el.text() + '\n'
        discount_2 = discount_2.strip()
        discount_discription = f'【 活動內容 】:{discount_1}【 活動期間 】：【 活動說明 】：{discount_2} ＊活動網址：'
        for el in dom('div.property_item').items():
            phone = el('p.small-text a').text()
            small_text_el = el('p.small-text')
            small_text_el.remove('a')
            address = small_text_el.text()
            place_id = find_place_id(address)
            info = get_place_info(place_id)
            if info:
                address = info.get('address', address)
                lat = info.get('lat', None)
                lon = info.get('lon', None)
            sub_name = el('h3.title-sin_map').text()
            name = f'{main_name}  {sub_name}'
            rettt = {'store': {'name': name, 'phone': phone, 'address': address, 'latitude': lat, 'longitude': lon, 'store_type': store_type},
                     'storediscount': {'name': discount_name, 'description': discount_discription},
                     'store_image': {'picture': img}}
            retttt.append(rettt)
            print(
                name,
                phone,
                address,
                lat,
                lon,
            )
    with open('./1111_crawlwer.json', 'w') as f:
        f.write(json.dumps(retttt))


if __name__ == '__main__':
    crawlwer_1111()
