from crawler import reids_wraper
from run_init import *

# 把template or 其他 所有的cache 都清除掉 常用來部署的時候 把cache 清除掉
for key in reids_wraper.r.keys():
    reids_wraper.r.delete(key)
