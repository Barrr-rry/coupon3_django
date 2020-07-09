from crawler import reids_wraper
from run_init import *

for key in reids_wraper.r.keys():
    reids_wraper.r.delete(key)
