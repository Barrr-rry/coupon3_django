import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.contrib.auth.models import User
from api import serializers
from api.models import StoreType, County, District, Store, DiscountType, StoreDiscount, StoreImage, Activity
from django.utils import timezone
import datetime
import random
from fake_data import cn_name, en_name, get_random_letters, get_random_number
import json
from django.utils.timezone import make_aware
from munch import Munch

fmt = '%Y-%m-%d %H:%M:%S'
test_email = 'max@conquers.co'


def main(for_test=False, config_data=None):
    generate_super_admin()
    generate_stort_type(5)
    generate_county()
    generate_district()
    generate_discount_type(5)
    generate_store()
    # generate_store_discount()
    # generate_store_image()
    generate_activity(5)


def generate_super_admin():
    from django.contrib.auth.models import User

    # create admin
    if not User.objects.first():
        user = User.objects.create_user('admin', password='1111')
        user.is_superuser = True
        user.is_staff = True
        user.save()


def generate_stort_type(count):
    names = [
        ('美食', 'cutlery.svg', 'cutlery_replace.svg'),
        ('住宿', 'double-bed.svg', 'double-bed_replace.svg'),
        ('娛樂', 'guitar.svg', 'guitar_replace.svg'),
        ('租賃', 'rent-a-car.svg', 'rent-a-car_replace.svg'),
        ('購物', 'shopping-bag.svg', 'shopping-bag_replace.svg'),
        ('旅遊', 'dumbbell.svg', 'dumbbell_replace.svg'),
        ('刷卡', 'cocktail.svg', 'cocktail_replace.svg'),
        ('美妝便利店', 'park.svg', 'park_replace.svg'),
        ('其他', 'other.svg', 'other_replace.svg'),
    ]
    for name, icon, replace_icon in names:
        StoreType.objects.create(
            name=name,
            icon=icon,
            replace_icon=replace_icon,
        )


def generate_county():
    county = ''
    with open('./county.txt') as f:
        county = f.read()
    county = county.split('\n')
    for el in county:
        target = el.split(',')
        County.objects.create(
            name=target[0],
            latitude=target[2],
            longitude=target[1],
            picture='景點照片_劍湖山.jpg'

        )


def generate_district():
    location = ''
    with open('./location.txt') as f:
        location = f.read()
    location = location.split('\n')
    for el in location:
        target = el.split(',')
        countys = County.objects.all()
        for county in countys:
            if county.name == target[0][:3]:
                district = target[0][3:]
                District.objects.create(
                    name=district,
                    county=county,
                    latitude=target[2],
                    longitude=target[1]
                )


def get_json(filename):
    import json

    ret = []
    with open(filename) as f:
        return json.loads(f.read())


def set_json(filename, data):
    import json

    ret = []
    with open(filename, 'w') as f:
        f.write(json.dumps(data))


def site1():
    data = get_json('./site1.json')

    store_type = StoreType.objects.all()
    store_dct = dict()
    for el in store_type:
        print(el.id, el.name)
        store_dct[el.name] = el.id
    store_map = {
        '餐飲美食': '美食',
        '流行時尚': '購物',
        '百貨商城': '購物',
        '美妝保養': '美妝便利店',
        '觀光工廠': '旅遊',
        '旅遊休憩': '旅遊',
        '其他': '其他',
        '': '其他',
        '居家生活': '購物',
    }
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.filter(name='抵用券').first()
    county_id = None
    district_id = None
    activity = Activity.objects.create(
        name='高雄振興購物嘉年華',
    )
    county_id_set = set()
    for el in data:
        addr = el['address']
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                county_id_set.add(county_id)
                break
        instance = Store.objects.create(
            name=el['name'],
            address=el['address'],
            store_type_id=store_dct[store_map[el['store_type']]],
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
            phone=None,
        )
        activity.store.add(instance)
        StoreDiscount.objects.create(
            store=instance,
            discount_type=discount_type,
            name='可使用高雄振興購物嘉年華抵用券',
            description='活動內容：本商家可使用抵用券（每張面額抵用50元），每筆消費不限張數，惟不得找零，亦不得兌換成現金。<br>活動日期：為109年6月1日（一）10：00 至 109 年 9 月 10 日（四）24：00止，逾期恕無法折抵使用。<br>活動辦法：https://www.lovekhshopping.com.tw/about4.php',
        )
        if el['storediscount']:
            StoreDiscount.objects.create(
                store=instance,
                discount_type=discount_type,
                name=None,
                description=el['storediscount']
            )
    for pk in county_id_set:
        activity.county.add(County.objects.get(pk=pk))
    activity.save()


def site2():
    data = get_json('./site2.json')

    storetype = StoreType.objects.filter(name='旅遊').first()
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.filter(name='補貼').first()
    county_id = None
    district_id = None
    county_id_set = set()
    activity = Activity.objects.create(
        name='鐵定貼心'
    )
    for el in data:
        addr = el['address']
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                county_id_set.add(county_id)
                break

        instance = Store.objects.create(
            name=el['name'],
            address=el['address'],
            store_type_id=storetype.id,
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
        )
        activity.store.add(instance)
        StoreDiscount.objects.create(
            store=instance,
            discount_type=discount_type,
            name='參觀本景點及住當地民宿每人補貼 500 元',
            description='活動內容：參加屏東縣三天兩夜 10 人以上團體行程（行程中含本景點），並於行程中入住兩晚屏東縣合法旅宿，每人獎助500元，每團補助上限1萬元整<br>活動日期：出發日期限定為6月15日至7月15日，貼心支持國內團體安心遊!<br>申請方式：依「屏東縣政府獎助旅行業推動國民旅遊實施要點」所定要件辦理完成後，於109年8月31日前備妥相關文件向本府申請獎助。<br>活動辦法：https://www.pthg.gov.tw/traffic/cp.aspx?n=FCA8BB125A1786AC&s=3D44C32E03E3DF25'
        )

    for pk in county_id_set:
        activity.county.add(County.objects.get(pk=pk))
    activity.save()


def from_csv():
    data = get_json('./csv.json')

    storetype = StoreType.objects.filter(name='旅遊').first()
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.first()
    county_id = None
    district_id = None
    for el in data:
        addr = el['address']
        if not addr:
            continue
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                break

        instance = Store.objects.create(
            name=el['name'],
            address=el['address'],
            store_type_id=el['store_type'],
            person=el['person'],
            email=el['email'],
            website=el['website'],
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
        )
        if el['discountype'] and el['discount_name']:
            StoreDiscount.objects.create(
                store=instance,
                discount_type_id=el['discountype'],
                name=el['discount_name'],
                description=el['description']
            )


def site3():
    data = get_json('./site3.json')

    storetype = StoreType.objects.filter(name='住宿').first()
    querset = District.objects.all()
    district_dct = dict()
    for el in querset:
        district_dct[el.name] = el
    discount_type = DiscountType.objects.first()
    county_id = None
    district_id = None
    county = None
    activity_tainan = Activity.objects.create(
        name='住台南百萬抽大獎',
    )
    activity_tainan.county.add(County.objects.filter(name='臺南市').first())
    activity_hualien = Activity.objects.create(
        name='住宿抽豐田汽車',
    )
    activity_hualien.county.add(County.objects.filter(name='花蓮縣').first())
    for el in data:
        addr = el['address']
        if not addr:
            continue
        for key in district_dct:
            if key in addr:
                district_id = district_dct[key].id
                county_id = district_dct[key].county_id
                county = district_dct[key].county
                break
        else:
            print('address...oops')
            continue

        if '台南' not in county.name and '花蓮' not in county.name:
            continue
        if el['lat'] == 'NaN' or el['lon'] == 'NaN':
            print('oops...')
            continue
        instance = Store.objects.create(
            store_type_id=storetype.id,
            name=el['title'],
            address=el['address'],
            latitude=el['lat'],
            longitude=el['lon'],
            county_id=county_id,
            district_id=district_id,
            status=1,
        )
        if '台南' in county.name:
            activity_tainan.store.add(instance)
            StoreDiscount.objects.create(
                store=instance,
                discount_type=DiscountType.objects.filter('抽獎').first(),
                name='6-8月月抽百萬大獎好禮',
                description='於6-8月入住台南各合法旅宿業者，登錄發票(或收據)即可參加6-8月月抽百萬大獎活動。<BR>單筆發票(或收據)登錄金額需滿500元以上，每滿500元即可得到1組抽獎序號（滿1000元，可得到2組抽獎序號，以此類推，每單筆發票至多可得到200組抽獎序號，不得與其他發票併計）。<BR>活動連結：https://tainanday.tw/index.php?action=act_mothod'
            )
            StoreDiscount.objects.create(
                store=instance,
                discount_type=DiscountType.objects.filter('登錄送').first(),
                name='住宿金額前十名贈 10000 元',
                description='尋找6-8月住宿台南的常客與貴人：<BR>活動內容：6-8月累積住宿台南金額最高的前十名民眾，且累積住宿天數不同日期達3日以上者，加碼贈新臺幣1萬元整獎勵金。<BR>活動期間：109年6月1日起至8月31日止，以個人登錄本活動網站之累計金額與實際住宿發票(收據)正本合計與驗證，若符合活動資格者超過十名民眾，同樣金額者將由系統電腦抽籤決定得獎者。<BR>活動連結：https://tainanday.tw/index.php?action=act_mothod'
            )
            StoreDiscount.objects.create(
                store=instance,
                discount_type=DiscountType.objects.filter(name='登錄送').first(),
                name='登錄即贈台南好物',
                description='登錄即贈限量台南特色好物<BR>活動內容：於活動網站登錄住宿台南發票(收據)之前1,000名民眾，即可獲贈限量台南特色好物(隨機贈送，不提供挑選)。<BR>活動說明：依民眾登錄活動網站系統的時間排序，前1,000名民眾(可重複得獎，多住多機會)，即可獲贈六甲蓮花茶、東山咖啡、玉井芒果乾、將軍虱目魚鬆、善化芝麻麵、新市火龍果麵、後壁茄芷袋、關子嶺旅行組等8種贈品其中一種(隨機贈送，不提供挑選，品項市價新臺幣140元至220元不等)，登錄時間次序以網站伺服器系統時間為準。<BR>活動連結：https://tainanday.tw/index.php?action=act_mothod (edited)'
            )
        if '花蓮' in county.name:
            activity_hualien.store.add(instance)
            """
            discount type ： 抽獎（請轉換成 ID）
            折扣標題：住宿抽豐田汽車
            折扣敘述：
            活動名稱：玩花蓮，抽豐田<BR>活動內容：活動期間在花蓮縣合法旅宿業住宿，並登錄相關資料，即享有抽獎機會，獎品為豐田汽車TOYOTA-YARIS 乙台。<BR>活動期間：109年6月20日起至109年11月15日止。(最後住宿日為109年11月15日、11月16日退房)。<BR>活動連結：https://trip.hl.gov.tw/#/explain
            """
            StoreDiscount.objects.create(
                store=instance,
                discount_type=DiscountType.objects.filter(name='抽獎').first(),
                name='住宿抽豐田汽車',
                description='玩花蓮，抽豐田<BR>活動內容：活動期間在花蓮縣合法旅宿業住宿，並登錄相關資料，即享有抽獎機會，獎品為豐田汽車TOYOTA-YARIS 乙台。<BR>活動期間：109年6月20日起至109年11月15日止。(最後住宿日為109年11月15日、11月16日退房)。<BR>活動連結：https://trip.hl.gov.tw/#/explain'
            )

    activity_hualien.save()
    activity_tainan.save()


def generate_store():
    # todo 要依照地址做filter 判斷有沒有被爬過
    site1()
    site2()
    site3()
    # from_csv()


def generate_discount_type(count):
    discount = ['打折',
                '贈品',
                '買就送',
                '滿減',
                '優惠碼',
                '抵用券',
                '補貼',
                '抽獎',
                '登錄送',
                '尊享服務',
                '優惠', ]
    for i in discount:
        DiscountType.objects.create(
            name=i,
        )


def generate_activity(count):
    county_query = County.objects.all()
    for county in county_query:
        activity = Activity.objects.create(
            name=f'{county.name}振興嘉年華',
        )
        activity.county.add(county)
        stores = Store.objects.filter(status=1, county=county).all()
        for s in stores:
            if random.choice([True, False]):
                activity.store.add(s)
        activity.save()


def generate_store_discount():
    stores = Store.objects.all()
    discount_types = DiscountType.objects.all()
    for store in stores:
        StoreDiscount.objects.create(
            store=store,
            discount_type=random.choice(discount_types),
            name='折扣標題',
            description='敘述',
        )


def generate_store_image():
    stores = Store.objects.all()
    for store in stores:
        for pic in ['景點_安平古堡.jpg', '景點照片_劍湖山.jpg', '景點照片_台北心潮飯點.jpg',
                    '景點照片_日月潭.jpg', '景點照片_野柳.jpg', '景點照片_金城武樹.jpg']:
            StoreImage.objects.create(
                store=store,
                picture=pic
            )


if __name__ == '__main__':
    main()
