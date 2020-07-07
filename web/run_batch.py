from run_init import *
from django.db import transaction

with transaction.atomic():
    StoreType.objects.filter(name='夜市').update(name='夜市商圈')


