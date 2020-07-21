from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import redis
import pickle
import uuid
from log import logger
from pyquery import PyQuery as pq
from api.util import get_time
"""
此module 主要是做map 爬蟲
"""

r = redis.StrictRedis(host='coupon3-redis')


class FIFOqueue:
    """
    利用 queue 做先進先出 每一次執行一個任務
    """

    def __init__(self, r):
        self.key = 'QueueTask'
        self.r = r

    def enqueue(self, task_type, task_args, task_id):
        """
        task_type
        task_args
        task_id: for return
        """
        item = (task_type, task_args, task_id)
        return self.r.rpush(self.key, pickle.dumps(item))

    def dequeue(self):
        ret = self.r.lpop(self.key)
        if ret:
            ret = pickle.loads(ret)
        return ret


class RedisWrap:
    def __init__(self, r):
        self.r = r

    def set(self, task_id, result):
        self.r.set(task_id, pickle.dumps(result))

    def get(self, task_id):
        ret = self.r.get(task_id)
        if ret:
            ret = pickle.loads(self.r.get(task_id))
        return ret


queue = FIFOqueue(r)
reids_wraper = RedisWrap(r)


class Task:
    """
    主要透過task 傳送任務 讓任務可以在crawler & 其他需要gps 的地方可以溝通
    並且將過去資料存入redis 減少運算時間
    """
    def __init__(self):
        pass

    def get_task_queue(self):
        tasks = queue.dequeue()
        return tasks

    def enqueue_task(self, task_type, task_args):
        # key 就是task_id
        key = task_type + task_args
        target = reids_wraper.get(key)
        if target:
            reids_wraper.set(key, target)
        else:
            queue.enqueue(task_type, task_args, key)
        return key

    def set_task_response(self, task_id, result):
        reids_wraper.set(task_id, pickle.dumps(result))

    def get_task_result(self, task_id):
        ret = reids_wraper.get(task_id)
        if ret:
            ret = pickle.loads(ret)
        return ret


task = Task()


def get_driver():
    # selenium 初始化資料
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--load-images=no")
    chrome_options.add_argument("--disk-cache=yes")
    chrome_options.add_argument("--ignore-ssl-errors=true")
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "permissions.default.stylesheet": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_latlon(driver, addr):
    # 抓取經緯度
    search = driver.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(1)
    doc = driver.page_source
    dom = pq(doc)
    lat = dom("#markercm").eq(-1).attr('y')
    lon = dom("#markercm").eq(-1).attr('x')
    address = dom('#markercm').eq(-1).attr('contenttip')
    return dict(
        gps=[lat, lon],
        address=address,
        count=len(dom('#markercm'))
    )


def get_addr(driver, latlon_str):
    """
    lat lon
    latlon_str = f'{lat}, {lon}'
    """
    # # 抓取address
    search = driver.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(latlon_str)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(1)
    doc = driver.page_source
    dom = pq(doc)
    lat = dom("#markercm").eq(-1).attr('y')
    lon = dom("#markercm").eq(-1).attr('x')
    address = dom('#markercm').eq(-1).attr('contenttip')
    return dict(
        gps=[lat, lon],
        address=address,
        count=len(dom('#markercm'))
    )


def loop_queue():
    driver = get_driver()
    driver.get("http://www.map.com.tw/")
    logger.info('get driver')
    # 重新整理
    reflash = False
    while True:
        tasks = task.get_task_queue()
        if not tasks:
            if reflash:
                driver.get("http://www.map.com.tw/")
                logger.info('reflash driver')
                reflash = False
            continue
        st = time.time()
        (task_type, task_args, task_id) = tasks
        # 有資料就不要再跑了 減少效能消耗
        if task.get_task_result(task_id):
            continue
        logger.info(f'task type:{task_type} args:{task_args}')
        if len(task_args) <= 1:
            logger.info(f'task_args too small: {task_args}')
            continue
        fn = get_addr if task_type == 'get_addr' else get_latlon
        dct = fn(driver, task_args)
        count = dct['count']
        # 如果一直增加搜尋紀錄 超過20 個 沒有人要資料的時候 就重新reflash
        if count > 20:
            reflash = True
        task.set_task_response(task_id, dct)
        ed = time.time()
        logger.info(f'task={tasks} ret={dct} time: {ed - st}')

    driver.quit()


if __name__ == '__main__':
    # task.enqueue_task('get_latlon', '高雄市中正四路148號')
    # task.enqueue_task('get_latlon', '高雄市中正三路42號')
    # task.enqueue_task('get_latlon', '高雄市中正三路44號')
    # task.enqueue_task('get_latlon', '高雄市中正三路46號')

    # task.enqueue_task('get_addr', '24.43353253, 118.3172157')

    logger.info('execute loop queue')
    while True:
        try:
            loop_queue()
        except Exception as e:
            logger.warning(f'Exception: {e}')
