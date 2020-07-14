from run_init import *
from django.db import transaction
import json

with transaction.atomic():
    querset = StoreDiscount.objects.filter(picture='True')
    for el in querset:
        el.picture = None
        el.save()
    querset = StoreImage.objects.filter(picture='True')
    for el in querset:
        el.picture = None
        el.save()

    queryset = StoreDiscount.objects.all()
    for el in queryset:
        if el.picture and len(el.picture) == 1:
            el.picture = None
            el.save()
        store = Store.objects.filter(id=el.store_id)
        if not store:
            print(f'remove dis id: {el.id} store id: {el.store_id}')
            # el.delete()
