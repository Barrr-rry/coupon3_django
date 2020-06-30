from run_init import *

import math

"""
"lat": "24.635421", "lon": "121.750068"
"""
import random
import re

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from munch import AutoMunch



msg = '高雄市中中正四路148號'
city_re = "|".join(city_list)
site_re = "|".join(site_list)
road_re = "|".join(road_list)
import time
ts = time.time()
target = re.findall(road_re, msg)
te = time.time()
print(te-ts)
road_dict[target[0]]

print()
