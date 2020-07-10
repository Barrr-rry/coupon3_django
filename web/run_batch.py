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