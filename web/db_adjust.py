from run_init import *

import math
from django.db import transaction

"""
"lat": "24.635421", "lon": "121.750068"
"""
import random
import re

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from munch import AutoMunch
from google import find_place_id, get_place_info, get_photo
from log import logger

queryset = Activity.original_objects.all()
for el in queryset:
    if el.store.count() == 0:
        el.delete()
        print(el.id)

print()
