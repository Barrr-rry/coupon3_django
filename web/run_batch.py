from run_init import *
from django.db import transaction
import json

with transaction.atomic():
    with open('./credit.json') as f:
        data = json.loads(f.read())
        for el in data:
            store = Store.objects.create(
                store_type_id=el['store_type_id'],
                status=el['status'],
                search_status=el['search_status'],
                name=el['name'],
                website=el['website'],
            )
            StoreImage.objects.create(
                store=store,
                picture=el['store_image_picture']
            )
            for dis in el['store_discount']:
                StoreDiscount.objects.create(
                    store=store,
                    discount_type_id=dis['discount_type_id'],
                    name=dis['name'],
                    description=dis['description'],
                    picture=el['store_image_picture']
                )
