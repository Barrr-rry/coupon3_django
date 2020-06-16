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

    def set(self, task_id, result, ex=60 * 60):
        self.r.set(task_id, pickle.dumps(result), ex=ex)

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
    # chrome_option s.add_argument("--disable-extensions")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_latlon(driver, addr):
    search = driver.find_element_by_id("searchWord")
    search.clear()
    search.send_keys(addr)
    driver.find_element_by_xpath("/html/body/form/div[10]/div[2]/img[2]").click()
    time.sleep(1)
    iframe = driver.find_elements_by_tag_name("iframe")[1]
    driver.switch_to.frame(iframe)
    coor_btn = driver.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    coor_btn.click()
    coor = driver.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr[2]/td")
    coor = coor.text.strip().split(" ")
    lat = coor[-1].split("：")[-1]
    log = coor[0].split("：")[-1]
    return lat, log


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
    iframe = driver.find_elements_by_tag_name("iframe")[1]
    driver.switch_to.frame(iframe)
    coor_btn = driver.find_element_by_xpath("/html/body/form/div[4]/table/tbody/tr[3]/td/table/tbody/tr/td[2]")
    coor_btn.click()
    el = driver.find_element_by_css_selector('span.highLightTxt')
    ret = el.text
    return ret


def loop_queue():
    driver = get_driver()
    while True:
        tasks = task.get_task_queue()
        if not tasks:
            time.sleep(1)
            continue
        (task_type, task_args, task_id) = tasks
        fn = get_addr if task_type == 'get_addr' else get_latlon
        driver.get("http://www.map.com.tw/")
        ret = fn(driver, task_args)
        logger.info(f'task={tasks} ret={ret}')
        task.set_task_response(task_id, ret)

    driver.quit()


if __name__ == '__main__':
    # task.enqueue_task('get_latlon', '高雄市中正四路148號')
    # task.enqueue_task('get_latlon', '高雄市中正四路148號')

    # queue.enqueue('get_latlon', '高雄市中正四路148號', str(uuid.uuid4()))
    # queue.enqueue('get_latlon', '高雄市中正四路148號', str(uuid.uuid4()))
    logger.info('execute loop queue')
    loop_queue()
