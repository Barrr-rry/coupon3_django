import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
import requests
from api.models import Traffic, Oil
import requests
from pyquery import PyQuery as pq
import re
import datetime
from django.utils.timezone import make_aware
from django.db.models import Q
from requests import adapters
import ssl
from urllib3 import poolmanager
from api.cron import get_oil, get_traffic, get_api1, get_api2, get_api3, get_api4, get_api5, get_api6, get_api7
from api.util import pickle_redis, session, to_datetime, none_or_text, get_url
from munch import AutoMunch

# get_api1()
# get_api2()
# get_api3()
# get_api4()
# get_api5()
# get_api6()
# get_api7()

now = datetime.datetime.now()
lat = 22.631505
lon = 120.296738
city = '高雄市'
location_sortd = lambda x: (abs(float(x['lat']) - lat) ** 2 + abs(float(x['lon']) - lon) ** 2) ** (1 / 2)


def get_element(loc, key, out_key):
    return list(filter(lambda x: x['elementName'] == key, loc['weatherElement']))[0][out_key]


def get_wather(lat, lon, city):
    weather = dict(
        temp=None,
        maxT=None,
        minT=None,
        weekMaxT=[],
        weekMinT=[],
        weekWx=[],
    )

    def get_future_list(data, day=True):
        ret = []
        key = '06:00' if day else '18:00'
        for el in data:
            start = to_datetime(el['startTime'][:-3])
            if start.date() > now.date() and key in el['startTime']:
                ret.append(el)
        return ret

    key = 'weather_info'
    data1 = pickle_redis.get_data(key)
    location = data1['records']['location']
    location = sorted(location, key=location_sortd)

    for loc in location:
        temp = float(get_element(loc, key='TEMP', out_key='elementValue'))
        maxT = float(get_element(loc, key='D_TX', out_key='elementValue'))
        minT = float(get_element(loc, key='D_TN', out_key='elementValue'))
        if temp and maxT and minT:
            weather['temp'] = round(temp)
            weather['maxT'] = round(maxT)
            weather['minT'] = round(minT)
            break
    key = 'weather_week'
    data5 = pickle_redis.get_data(key)
    location = data5['records']['locations'][0]['location']
    location = sorted(location, key=location_sortd)

    for loc in location:
        maxt = get_element(loc, key='MaxT', out_key='time')
        maxt = get_future_list(maxt)
        maxt = list(map(lambda x: dict(
            startTime=x['startTime'],
            endTime=x['endTime'],
            value=x['elementValue'][0]['value']
        ), maxt))
        weather['weekMaxT'] = maxt

        mint = get_element(loc, key='MinT', out_key='time')
        mint = get_future_list(mint, day=False)
        mint = list(map(lambda x: dict(
            startTime=x['startTime'],
            endTime=x['endTime'],
            value=x['elementValue'][0]['value']
        ), mint))
        weather['weekMinT'] = mint

        wx = get_element(loc, key='Wx', out_key='time')
        wx = get_future_list(wx)
        wx = list(map(lambda x: dict(
            startTime=x['startTime'],
            endTime=x['endTime'],
            value=x['elementValue'][0]['value']
        ), wx))
        weather['weekWx'] = wx
    return weather


def get_aqi(lat, lon, city):
    location_sortd = lambda x: (abs(float(x['Latitude']) - lat) ** 2 + abs(float(x['Longitude']) - lon) ** 2) ** (1 / 2)
    aqi = {
        "aqi": None,
        "pm25": None,
        "pm10": None,
        "o3": None,
    }
    key = 'weather_aqi'
    data2 = pickle_redis.get_data(key)
    data2 = sorted(data2, key=location_sortd)
    for el in data2:
        if all([el['AQI'], el['PM2.5'], el['PM10'], el['O3']]):
            aqi['aqi'] = float(el['AQI'])
            aqi['pm25'] = float(el['PM2.5'])
            aqi['pm10'] = float(el['PM10'])
            aqi['o3'] = float(el['O3'])
            break
    return aqi


def get_uvi(lat, lon, city):
    key = 'weather_uv'
    data3 = pickle_redis.get_data(key)
    for el in data3:
        latlist = el['WGS84Lat'].split(',')
        lonlist = el['WGS84Lon'].split(',')
        lat = float(latlist[0]) + float(latlist[1]) / 60 + float(latlist[2]) / 3600
        lon = float(lonlist[0]) + float(lonlist[1]) / 60 + float(lonlist[2]) / 3600
        el['lat'] = lat
        el['lon'] = lon

    data3 = sorted(data3, key=location_sortd)
    for el in data3:
        if el['UVI']:
            return float(el['UVI'])


def get_rain(lat, lon, city):
    ret = {
        "pop": None,
    }
    key = 'weather_rain_percent'
    data4 = pickle_redis.get_data(key)
    for el in data4['records']['location']:
        if el['locationName'] == city:
            ret['pop'] = float(get_element(el, key='PoP', out_key='time')[0]['parameter']['parameterName'])
            break
    return ret


def get_desc(lat, lon, city):
    key = 'weather_helper'
    data7 = pickle_redis.get_data(key)
    return list(
        map(lambda x: dict(description=x['parameterValue']),
            data7[city]['cwbopendata']['dataset']['parameterSet']['parameter']))


ret = get_desc(lat, lon, city)
print()

print()
