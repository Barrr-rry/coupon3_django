from run_init import *
from django.db import transaction
import json
import os
from PIL import Image
import re

data = []
old_name = '參觀本景點及住當地民宿每人補貼 500 元'
new_name = '參觀本景點及住民宿每人補貼 500 元'
desc = """【 活動內容 】：參觀本景點及住民宿每人補貼 500 元

【 活動期間 】：2020/6/15 ~ 2020/7/15

【 活動說明 】：

＊參加屏東縣三天兩夜 10 人以上團體行程（行程中含本景點），並於行程中入住兩晚屏東縣合法旅宿，每人獎助500元。

＊每團補助上限1萬元整。

＊申請方式：依「屏東縣政府獎助旅行業推動國民旅遊實施要點」所定要件辦理完成後，於109年8月31日前備妥相關文件向本府申請獎助。

＊活動網址：https://www.pthg.gov.tw/traffic/cp.aspx?n=FCA8BB125A1786AC&s=3D44C32E03E3DF25

"""
data.append((old_name, new_name, desc))

# ---------------------------------------------------------
old_name = '住宿抽豐田汽車'
new_name = '住宿抽豐田汽車'
desc = """【 活動內容 】：玩花蓮，抽豐田

【 活動期間 】：2020/6/20 ~ 2020/11/15

【 活動說明 】：

＊活動期間在花蓮縣合法旅宿業住宿，並登錄相關資料，即享有抽獎機會。

＊獎品為豐田汽車TOYOTA-YARIS 乙台。

＊最後住宿日為109年11月15日、11月16日退房。

＊活動網址：https://trip.hl.gov.tw/#/explain"""
data.append((old_name, new_name, desc))

# ---------------------------------------------------------
old_name = '登錄即贈台南好物'
new_name = '登錄即贈台南好物'
desc = """【 活動內容 】：6-8月月抽百萬大獎好禮

【 活動期間 】：2020/6/1 ~ 2020/8/31

【 活動說明 】：

＊於6-8月入住台南各合法旅宿業者，登錄發票(或收據)即可參加6-8月月抽百萬大獎活動。

＊單筆發票(或收據)登錄金額需滿500元以上，每滿500元即可得到1組抽獎序號（滿1000元，可得到2組抽獎序號，以此類推）。

＊每單筆發票至多可得到200組抽獎序號，不得與其他發票併計。

＊活動網址：https://tainanday.tw/index.php?action=act_mothod"""
data.append((old_name, new_name, desc))

# ---------------------------------------------------------
old_name = '住宿金額前十名贈 10000 元'
new_name = '住宿金額前十名贈 10000 元'
desc = """【【 活動內容 】：尋找6-8月住宿台南的常客與貴人

【 活動期間 】：2020/6/1 ~ 2020/8/31

【 活動說明 】：

＊6-8月累積住宿台南金額最高的前十名民眾，且累積住宿天數不同日期達3日以上者，加碼贈新臺幣1萬元整獎勵金。

＊以個人登錄本活動網站之累計金額與實際住宿發票(收據)正本合計與驗證，若符合活動資格者超過十名民眾，同樣金額者將由系統電腦抽籤決定得獎者。

＊活動網址：https://tainanday.tw/index.php?action=act_mothod"""
data.append((old_name, new_name, desc))

# ---------------------------------------------------------
old_name = '6-8月月抽百萬大獎好禮'
new_name = '6-8月月抽百萬大獎好禮'
desc = """【 活動內容 】：6-8月月抽百萬大獎好禮

【 活動期間 】：2020/6/1 ~ 2020/8/31

【 活動說明 】：

＊入住台南各合法旅宿業者，登錄發票(或收據)即可參加6-8月月抽百萬大獎活動。

＊單筆發票(或收據)登錄金額需滿500元以上，每滿500元即可得到1組抽獎序號（滿1000元，可得到2組抽獎序號，以此類推。

＊每單筆發票至多可得到200組抽獎序號，不得與其他發票併計。

＊活動網址：https://tainanday.tw/index.php?action=act_mothod"""
data.append((old_name, new_name, desc))

# ---------------------------------------------------------
old_name = '住宿送免費雙層觀巴 - 安心旅宿 X 雙層觀巴'
new_name = '住宿送免費雙層觀巴'
desc = """【 活動內容 】：住宿送免費雙層觀巴＊安心旅宿 X 雙層觀巴

【 活動期間 】：2020/7/1 ~ 2020/10/31

【 活動說明 】：

＊凡入住安心旅館，當次每房住宿費滿千，即可獲贈限量「雙層觀光巴士24小時票券兌換券」。

＊每房贈送數量以「入住人數」為上限，每人限領1張，限量發送。

＊兌換券須於109年10月31日前使用。

＊活動網址：https://www.taipeisightseeing.com.tw/news/details/360"""
data.append((old_name, new_name, desc))

# ---------------------------------------------------------
old_name = '抽 500 元電子旅遊券'
new_name = '抽 500 元電子旅遊券'
desc = """【 活動內容 】：抽 500 元電子旅遊券

【 活動期間 】：2020/6/22 ~ 2020/6/29

【 活動說明 】：

＊6/22日 9:00 起至6/29日 18:00 止桃園市民登錄資料有機會獲500元電子旅遊券

＊活動網址：https://www.lovekhshopping.com.tw/about4.php"""
data.append((old_name, new_name, desc))
# ---------------------------------------------------------
old_name = '住宿最高補助 1,000 元'
new_name = '安心旅遊補助 1,000 元'
desc = """【 活動內容 】：住宿最高補助 1,000 元

【 活動期間 】：2020/7/1 ~ 2020/10/31

【 活動說明 】：

＊民眾入住參與活動的旅館或民宿，每房現場折抵住宿費最高 1,000 元，平假日都適用。

＊每房每日限用一次獎助金，每一身分證字號限使用 1 次。

＊活動懶人包：https://3coupon.info/eli5/tour/"""
data.append((old_name, new_name, desc))


# ---------------------------------------------------------
def update_data(old_name, new_name, desc):
    queryset = StoreDiscount.objects.filter(name=old_name)
    print(old_name, queryset.count())
    for el in queryset:
        el.name = new_name
        el.description = desc
        el.save()


# ---------------------------------------------------------
data2 = []
# ---------------------------------------------------------
gte_id = 3569
lte_id = 3577
old_name = '聯合商品券'
new_name = '聯合商品券買 8000 送 800'
desc = """【 活動內容 】：觀光旅館聯合商品券買 8000 送 800

【 活動期間 】：2020/6/1 ~ 2020/10/31

【 活動說明 】：

＊109年6月1日至109年10月31日 觀光旅館買8000送800。

＊加碼送升等房型或早餐券。

＊高雄市旅行公會整合7家旅行社共同聯合代售。

＊活動網址：https://khh.travel/zh-tw/event/news/3001"""
picture = None
data2.append((gte_id, lte_id, old_name, new_name, desc, picture))
# ---------------------------------------------------------
gte_id = 3578
lte_id = 3608
old_name = '聯合商品券'
new_name = '聯合住宿券買 8000 住七晚'
desc = """【 活動內容 】：一般旅館/汽車旅館聯合住宿券

【 活動期間 】：2020/6/1 ~ 2020/10/31

【 活動說明 】：

＊只要購買8000元即6張住宿券，觀光局則另加碼送出一張住宿券，共可住7晚。

＊高雄市旅行公會整合7家旅行社共同聯合代售。

＊活動網址：https://khh.travel/zh-tw/event/news/3001"""
picture = '國旅優惠方案EDM.jpg'
data2.append((gte_id, lte_id, old_name, new_name, desc, picture))
# ---------------------------------------------------------
gte_id = 3609
lte_id = 3615
old_name = '聯合商品券'
new_name = '販售聯合商品券買 8000 送 800'
desc = """【 活動內容 】：販售觀光旅館聯合商品券買 8000 送 800

【 活動期間 】：2020/6/1 ~ 2020/10/31

【 活動說明 】：

＊109年6月1日至109年10月31日 觀光旅館買8000送800。

＊加碼送升等房型或早餐券。

＊高雄市旅行公會整合7家旅行社共同聯合代售，共500套。

＊參與業者：漢來大飯店、高雄國賓大飯店、高雄福華大飯店、寒軒國際大飯店、麗尊酒店、福容大飯店、華園大飯店、義大皇家酒店、翰品酒店高雄，共計9家。

＊活動商家：https://3coupon.info/store_activity/?activity=30

＊活動網址：https://khh.travel/zh-tw/event/news/3001"""
picture = None
data2.append((gte_id, lte_id, old_name, new_name, desc, picture))


def update_data2(gte_id, lte_id, old_name, new_name, desc, picture):
    queryset = StoreDiscount.original_objects.filter(store__id__gte=gte_id, store__id__lte=lte_id)
    print(old_name, queryset.count())
    for el in queryset:
        el.name = new_name
        el.description = desc
        el.picture = picture
        el.save()


with transaction.atomic():
    for old_name, new_name, desc in data:
        update_data(old_name, new_name, desc)

    for gte_id, lte_id, old_name, new_name, desc, picture in data2:
        update_data2(gte_id, lte_id, old_name, new_name, desc, picture)
