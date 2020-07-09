from crawler import reids_wraper
from run_init import *


for key in reids_wraper.r.keys():
    reids_wraper.r.delete(key)


queryset = Store.objects.all()
data = json.dumps(serializers.StoreSerializer(many=True, instance=queryset).data)
reids_wraper.set(key, data)
