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
        logger.error(f'status error: code: {data["status"]} place_id: {place_id}')
        return ret
    data = data['result']
    ret = dict(
        address=data.get('formatted_address'),
        phone=data.get('formatted_phone_number'),
        website=data.get('website'),
        name=data['name'],
        lat=data['geometry']['location']['lat'],
        lon=data['geometry']['location']['lng'],
        photos=data.get('photos', [])
    )
    return ret


def get_photo(ref):
    url = 'https://maps.googleapis.com/maps/api/place/photo'
    r = requests.get(url, params=dict(
        maxwidth=640,
        photoreference=ref,
        key=key,
    ))
    ref = ref[:100]
    with open(f'./media/{ref}.jpeg', 'wb') as f:
        f.write(r.content)
    return f'{ref}.jpeg'


if __name__ == '__main__':
    # place_id = find_place_id('高雄大遠百')
    place_id = 'ChIJ-ZcUgXsDbjQRbi4wSNqqojk'
    ret = get_place_info(place_id)
    # photo_ref = 'CmRaAAAAI357j2YOOnaOspSVOjwUQZYwT7iE6Ag8Wrn159SKJaNbuq6ZytZCWXB3_iSbVQlvjyQV4ewiiJAIRZJChLSXTOrxiZRieQ3Ztu_h8mesxU2os6GTamtKGNRCbezwPHiYEhDIcfLW3BZOSvBfT2jn0lOZGhRCzCxxVQeHwzSkk76t_zYD_cZnZg'
    # photo = get_photo(photo_ref)
    print()
