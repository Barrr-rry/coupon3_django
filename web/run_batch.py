import pandas as pd
import numpy as np
import json
from run_init import *
from django.db import transaction, router
from log import logger
from google import find_place_id, get_place_info, get_photo

import re
import pandas as pd
import numpy as np
from google import find_place_id, get_place_info, get_photo
import math
from collections import defaultdict

queryset = Store.objects.filter(address__contains='台灣')
for el in queryset:
    if re.findall('\d+台灣', el.address):
        print(re.sub('\d+台灣', '', el.address), el.address)
        el.address = re.sub('\d+台灣', '', el.address)
        el.save()
queryset = Store.objects.filter(phone__contains='+886-')
for el in queryset:
    print(el.phone.replace('+886-', '0'), el.phone)
    el.phone = el.phone.replace('+886-', '0')
    el.save()
print()
