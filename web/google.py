import requests
import urllib.parse
from log import logger

key = 'AIzaSyB8SR12DJW0lrsurwa74PrCsfytq8BWqJc'


def find_place_id(msg):
    ret = ''
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    r = requests.get(url, params=dict(
        key=key, input=msg, inputtype='textquery'
    ))
    data = r.json()
    if data['status'] != 'OK':
        logger.error(f'status error: code: {data["status"]} msg: {msg}')
        return ret
    return data['candidates'][0]['place_id']


def get_place_info(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    r = requests.get(url, params=dict(
        key=key, place_id=place_id, language='zh-TW'
    ))
    ret = None
    data = r.json()
    if data['status'] != 'OK':
        logger.error(f'status error: code: {data["status"]} msg: {msg}')
        return ret
    data = data['result']
    ret = dict(
        address=data['formatted_address'],
        phone=data['formatted_phone_number'],
        website=data['website'],
    )
    return ret


if __name__ == '__main__':
    # place_id = find_place_id('高雄大遠百')
    place_id = 'ChIJ-ZcUgXsDbjQRbi4wSNqqojk'
    ret = get_place_info(place_id)
    print()
