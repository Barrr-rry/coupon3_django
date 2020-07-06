from run_init import *
from django.db import transaction

with transaction.atomic():
    play_store_type = StoreType.objects.filter(name='娛樂').first()
    rent_store_type = StoreType.objects.filter(name='租賃').first()
    nmarket_store_type = StoreType.objects.create(
        name='夜市',
        icon='night-mark.svg',
        replace_icon='night-mark_replace.svg'
    )
    play_store = Store.objects.filter(store_type=rent_store_type).all().count()
    rent_store = Store.objects.filter(store_type=play_store_type).all().count()
    if play_store or rent_store:
        raise Exception('要刪除的資料有store')
    play_store_type.delete()
    rent_store_type.delete()

    StoreType.objects.filter(name='旅遊').update(name='娛樂旅遊')
    StoreType.objects.filter(name='美妝便利店').update(name='連鎖店電商')
    StoreType.objects.filter(name='刷卡').update(name='刷卡電子支付')
