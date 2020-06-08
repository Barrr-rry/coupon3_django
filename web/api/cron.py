# from log import logger
import requests
from api.models import Oil, Traffic
import requests
from pyquery import PyQuery as pq
import re
import datetime
from django.utils.timezone import make_aware
from requests import adapters
import ssl
from urllib3 import poolmanager
from api.util import pickle_redis, session, to_datetime, none_or_text, get_url
import json


def get_oil():
    url = 'https://gas.goodlife.tw/'
    r = requests.get(url)
    doc = r.content
    dom = pq(doc)
    args = dict()
    keys = [
        'CPC_oil_92',
        'CPC_oil_95',
        'CPC_oil_98',
        'CPC_diesel_oil',
        'FPC_oil_92',
        'FPC_oil_95',
        'FPC_oil_98',
        'FPC_diesel_oil',
    ]
    for key, el in zip(keys, dom('#cpc > ul > li').items()):
        args[key] = el.text().split('\n')[-1]

    args['last_updated_at'] = re.findall(r'\d+-\d+-\d+ \d+:\d+', dom('p.update').text())[0]
    args['last_updated_at'] = make_aware(datetime.datetime.strptime(args['last_updated_at'], '%Y-%m-%d %H:%M'))

    text = dom('.main > h2').text()
    oil_change = re.sub(r'[\u4e00-\u9fa5_a-zA-Z]', '', text)
    oil_change = float(oil_change)
    oil_change = oil_change if '漲' in text else -oil_change
    args['oil_change'] = oil_change

    text = dom('#gas-price li.alt').eq(0).text()
    point = re.findall('[\d\.]+', text)[0]
    args['diesel_change'] = point if '+' in text else -point

    announce_status = '中油油價已公告' in dom('#gas-price li > p').text()
    args['announce_status'] = announce_status
    instance = Oil.objects.create(**args)


def get_traffic():
    page = 1
    url = f'https://road.ioi.tw/?&t=t1&p={page}'

    headers = {
        'authority': 'road.ioi.tw',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
        'cookie': '__cfduid=d55054d486b96d05121165bbe1f9c9e431591001499',
    }

    r = requests.get(url, headers=headers)
    doc = r.content
    dom = pq(doc)
    for el in dom('.card.bg-danger').items():
        el('span.badge.badge-info').text()
        card_body = el('.card-body')
        card_body.remove('span')
        el('span.uptime').text()
        el_href = el('.bg-danger > a')
        lat, long = None, None
        if el_href:
            lat, long = el_href.attr.href.split('q=')[-1].split(',')
        args = dict(
            data_type=none_or_text(el('span.badge.badge-warning').text()),
            region=none_or_text(el('span.badge.badge-info').text()),
            subject=card_body.text().split('\n')[0],
            from_created_at=to_datetime(el('span.happentime').text()),
            from_edit_at=to_datetime(el('span.uptime').text()),
            fake_id=el.attr.id,
            lat=lat,
            long=long,
        )
        target = Traffic.objects.filter(fake_id=args['fake_id']).first()
        if target:
            for key in args:
                setattr(target, key, args[key])
            target.save()
        else:
            instance = Traffic.objects.create(**args)


def get_api1():
    """
    取最近天氣資訊
    """
    url = 'http://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-CB4BCD6A-E710-4672-A9BF-8DB65AAA81CD&parameterName=CITY'
    r = get_url(url)
    key = 'weather_info'
    data = json.loads(r.text)
    pickle_redis.set_data(key, data)


def get_api2():
    """
    取空氣品質
    """
    url = 'https://opendata.epa.gov.tw/webapi/Data/AQI/?$skip=0&$top=1000&format=json'
    r = get_url(url)
    key = 'weather_aqi'
    data = json.loads(r.text)
    pickle_redis.set_data(key, data)


def get_api3():
    """
    取紫外線
    """
    url = 'https://opendata.epa.gov.tw/webapi/Data/UV/?$skip=0&$top=1000&format=json'
    r = get_url(url)
    key = 'weather_uv'
    data = json.loads(r.text)
    pickle_redis.set_data(key, data)


def get_api4():
    """
    取降雨機率
    """
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-CB4BCD6A-E710-4672-A9BF-8DB65AAA81CD'
    r = get_url(url)
    key = 'weather_rain_percent'
    data = json.loads(r.text)
    pickle_redis.set_data(key, data)


def get_api5():
    """
    取一週天氣
    """
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-CB4BCD6A-E710-4672-A9BF-8DB65AAA81CD'
    r = get_url(url)
    key = 'weather_week'
    data = json.loads(r.text)
    pickle_redis.set_data(key, data)


def get_api6():
    """
    取累積雨量
    """
    url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-CB4BCD6A-E710-4672-A9BF-8DB65AAA81CD'
    r = get_url(url)
    key = 'weather_rain'
    data = json.loads(r.text)
    pickle_redis.set_data(key, data)


def get_api7():
    """
    取天氣小幫手
    """
    locations_dct = {
        "台北市": "F-C0032-009",
        "新北市": "F-C0032-010",
        "基隆市": "F-C0032-011",
        "宜蘭縣": "F-C0032-013",
        "桃園市": "F-C0032-022",
        "新竹縣": "F-C0032-023",
        "新竹市": "F-C0032-024",
        "苗栗縣": "F-C0032-020",
        "台中市": "F-C0032-021",
        "彰化縣": "F-C0032-028",
        "南投縣": "F-C0032-026",
        "雲林縣": "F-C0032-029",
        "嘉義縣": "F-C0032-018",
        "嘉義市": "F-C0032-019",
        "台南市": "F-C0032-016",
        "高雄市": "F-C0032-017",
        "屏東縣": "F-C0032-025",
        "花蓮縣": "F-C0032-012",
        "台東縣": "F-C0032-027",
        "金門縣": "F-C0032-014",
        "連江縣": "F-C0032-030",
        "澎湖縣": "F-C0032-015"
    }
    ret = dict()
    for loc, key in locations_dct.items():
        url = f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/{key}?Authorization=CWB-CB4BCD6A-E710-4672-A9BF-8DB65AAA81CD&downloadType=WEB&format=JSON'
        r = get_url(url)
        data = json.loads(r.text)
        ret[loc] = data
    key = 'weather_helper'
    pickle_redis.set_data(key, ret)


def line_notify():
    msg = '我是測試'
    token = 'FtiyBzeoeH6OQ02pkgnh1A89LWW6SiCH04kqR0kV3nc'
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token
    }

    payload = {'message': msg}
    r = requests.post(url, headers=headers, params=payload)
