from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
# chrome_option s.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
print('before')
driver = webdriver.Chrome(options=chrome_options)
print('get driver')
driver.get("https://freelancerlife.info/")  # 前往這個網址
print('get url')
driver.close()  # 關閉瀏覽器
print('close')
