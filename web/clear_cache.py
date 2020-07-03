from crawler import reids_wraper


for key in reids_wraper.r.keys():
    reids_wraper.r.delete(key)