from run_init import *

for el in Store.objects.filter(latitude__isnull=True):
    el.status = 0
    el.save()
