import datetime
from django.forms import forms
from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser, PermissionsMixin
from rest_framework.authtoken.models import Token as DefaultToken
from rest_framework import exceptions
from django.utils import timezone
# from django.db import models
from django.contrib.gis.db import models
import uuid
from django.contrib.gis.geos import Point


class ParanoidQuerySet(models.QuerySet):
    """
    更改原本的queryset
    不要讓他刪除原本的資料
    """

    def real_delete(self):
        """
        真的要刪除再用這個function
        """
        return super().delete()

    def delete(self):
        """
        overwrite 原本delete 功能 改成 符合我們db 的格式
        """
        for obj in self:
            obj.deleted_status = True
            obj.deleted_at = timezone.now()
            obj.save()


class ParanoidManager(models.Manager):
    """
    預設queryset 自動filter deleted_status=False 的資料 這樣才不用每一個都還要額外寫
    """

    def get_queryset(self):
        return ParanoidQuerySet(self.model, using=self._db).filter(
            deleted_status=False)


class DefaultAbstract(models.Model):
    """
    每一個model 定義歐繼承此class 這樣就不用每一筆資料 用還要寫重複的東西
    """
    deleted_status = models.BooleanField(default=False, help_text='資料刪除狀態')
    created_at = models.DateTimeField(auto_now_add=True, help_text='建立時間')
    updated_at = models.DateTimeField(null=True, help_text='更新時間')
    deleted_at = models.DateTimeField(null=True, blank=True, help_text='刪除時間')
    # 覆蓋本來的objects
    objects = ParanoidManager()
    # 真的需要再改用這個方法
    original_objects = models.Manager()

    class Meta:
        abstract = True
        # ordering = ['-updated_at', '-created_at']
        # 預設排序 都從最新資料在前面
        ordering = ['-created_at']

    def real_delete(self, *args, **kwargs):
        # 真的要delete 在call this function
        return super().delete(*args, **kwargs)

    def delete(self, **kwargs):
        # overwrite delete function
        self.deleted_status = True
        self.deleted_at = timezone.now()
        self.save()


class StoreType(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="類型名稱")
    icon = models.CharField(max_length=128, help_text="標籤名稱")
    replace_icon = models.CharField(max_length=128, help_text="替代標籤")

    class Meta:
        ordering = ['created_at']


class County(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="縣市名稱")
    picture = models.CharField(max_length=128, help_text="縣市圖片")
    latitude = models.FloatField(max_length=64, help_text="經度")
    longitude = models.FloatField(max_length=64, help_text="緯度")


class District(DefaultAbstract):
    county = models.ForeignKey(County, related_name="district", on_delete=models.CASCADE, help_text="縣市fk")
    name = models.CharField(max_length=128, help_text="行政區名稱")
    latitude = models.FloatField(max_length=64, help_text="經度")
    longitude = models.FloatField(max_length=64, help_text="緯度")


class Store(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="商家名稱", null=True, blank=True)
    google_name = models.CharField(max_length=128, help_text="商家名稱", null=True, blank=True)
    store_type = models.ForeignKey(StoreType, related_name="store", on_delete=models.CASCADE, help_text="店家類型fk")
    phone = models.CharField(max_length=64, help_text="電話", null=True, blank=True)
    person = models.CharField(max_length=128, help_text="聯絡人", null=True, blank=True)
    email = models.CharField(max_length=128, help_text="信箱", null=True, blank=True)
    website = models.CharField(max_length=512, null=True, blank=True, help_text="網站")
    address = models.CharField(max_length=128, help_text="商家地址", null=True, blank=True)
    latitude = models.FloatField(max_length=64, help_text="經度", null=True, blank=True)
    longitude = models.FloatField(max_length=64, help_text="緯度", null=True, blank=True)
    location = models.PointField(null=True, blank=True, srid=4326, help_text='Location')
    county = models.ForeignKey(County, related_name="store", on_delete=models.CASCADE, help_text="縣市fk", null=True,
                               blank=True)
    district = models.ForeignKey(District, related_name="store", on_delete=models.CASCADE, help_text="行政區fk", null=True,
                                 blank=True)
    status = models.SmallIntegerField(default=0, help_text="商家狀態 0：待審核；1：審核通過（上架）；2：審核失敗（不顯示）")
    google_status = models.SmallIntegerField(default=0, help_text="from google 0: 沒有資料 1: 有資料")
    search_status = models.SmallIntegerField(default=1, help_text="0: 一般商店：但只有選擇活動才能被搜尋 1: 目前的一般搜尋 2: 信用卡搜尋")
    ad = models.TextField(default=None, null=True, blank=True, help_text='廣告')
    pop = models.IntegerField(default=0, help_text='人氣')

    def save(self, *args, **kwargs):
        # save 資料前 確認如果有經緯度 自動填上location 欄位 這樣才不會改太多程式碼
        if not self.location and self.latitude and self.longitude:
            self.location = Point(float(self.latitude), float(self.longitude), srid=4326)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # get url
        return f'/store/{self.pk}'


class Activity(DefaultAbstract):
    name = models.CharField(max_length=64, help_text="活動名稱")
    store = models.ManyToManyField(Store, related_name='activity')
    county = models.ManyToManyField(County, related_name='activity')
    description = models.TextField(help_text="敘述", null=True, blank=True)


class DiscountType(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="折扣名稱")


class StoreDiscount(DefaultAbstract):
    store = models.ForeignKey(Store, related_name="storediscount", on_delete=models.CASCADE, help_text="")
    discount_type = models.ForeignKey(DiscountType, related_name="store_discount", on_delete=models.CASCADE,
                                      help_text="折扣fk")
    name = models.CharField(max_length=128, null=True, blank=True, help_text="折扣標題")
    description = models.TextField(help_text="敘述", null=True, blank=True)
    picture = models.CharField(max_length=128, help_text="商家圖片", null=True, blank=True, default=None)


class StoreImage(DefaultAbstract):
    store = models.ForeignKey(Store, related_name="storeimage", on_delete=models.CASCADE, help_text="商家fk")
    picture = models.CharField(max_length=128, help_text="商家圖片", null=True, blank=True)


def validate_file(file):
    """
    後端驗證 檔案大小以及圖片格式
    """
    import re
    file_size = 1048576
    try:
        # 確定檔案格式
        content_type = file.content_type
        if re.findall('^image/.+?', content_type):
            if file.size > file_size:
                raise forms.ValidationError('超過 1MB，請重新上傳圖片')
        else:
            raise forms.ValidationError('圖片格式錯誤，請重新上傳圖片')
    except AttributeError:
        pass
    return True


class ConfigSetting(DefaultAbstract):
    in_maintenance = models.BooleanField(default=False, help_text="維護中")


class File(DefaultAbstract):
    file = models.FileField(validators=[validate_file])
