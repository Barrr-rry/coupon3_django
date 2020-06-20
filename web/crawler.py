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

r = redis.StrictRedis(host='coupon3-redis')


class FIFOqueue:

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
    search = driver.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(1)
    doc = driver.page_source
    dom = pq(doc)
    lat = dom("#markercm").eq(-1).attr('y')
    lon = dom("#markercm").eq(-1).attr('x')
    return dict(
        ret=[lat, lon],
        count=len(dom('#markercm'))
    )


def get_addr(driver, latlon_str):
    """
    lat lon
    latlon_str = f'{lat}, {lon}'
    """
    search = driver.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(latlon_str)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(1)
    doc = driver.page_source
    dom = pq(doc)
    ret = dom('#markercm').eq(-1).attr('contenttip')
    return dict(
        ret=ret,
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
        logger.info(f'task type:{task_type} args:{task_args}')
        if len(task_args) <= 1:
            logger.info(f'task_args too small: {task_args}')
            continue
        fn = get_addr if task_type == 'get_addr' else get_latlon
        dct = fn(driver, task_args)
        ret = dct['ret']
        count = dct['count']
        if count > 20:
            reflash = True
        task.set_task_response(task_id, ret)
        ed = time.time()
        logger.info(f'task={tasks} ret={ret} time: {ed - st}')

    driver.quit()


if __name__ == '__main__':
    task.enqueue_task('get_latlon', '高雄市中正四路148號')
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
