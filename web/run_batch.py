from run_init import *
from django.db import transaction
import json

with transaction.atomic():
    queryset = StoreImage.objects.all()
    for el in queryset:
        if el.picture and (len(el.picture) == 1 or el.picture == 'True'):
            el.picture = None
            el.save()
        store = Store.objects.filter(id=el.store_id)
        if not store:
            print(f'remove dis id: {el.id} store id: {el.store_id}')
            # el.delete()
