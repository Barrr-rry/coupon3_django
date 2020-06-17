import datetime

from django.contrib.auth.models import AbstractBaseUser, UserManager, AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.authtoken.models import Token as DefaultToken
from rest_framework import exceptions
from django.utils import timezone
import uuid


class ParanoidQuerySet(models.QuerySet):
    """
    Prevents objects from being hard-deleted. Instead, sets the
    ``date_deleted``, effectively soft-deleting the object.
    """

    def delete(self):
        for obj in self:
            obj.deleted_status = True
            obj.deleted_at = timezone.now()
            obj.save()


class ParanoidManager(models.Manager):
    """
    Only exposes objects that have NOT been soft-deleted.
    """

    def get_queryset(self):
        return ParanoidQuerySet(self.model, using=self._db).filter(
            deleted_status=False)


class DefaultAbstract(models.Model):
    deleted_status = models.BooleanField(default=False, help_text='資料刪除狀態')
    created_at = models.DateTimeField(auto_now_add=True, help_text='建立時間')
    updated_at = models.DateTimeField(null=True, help_text='更新時間')
    deleted_at = models.DateTimeField(null=True, blank=True, help_text='刪除時間')
    objects = ParanoidManager()
    original_objects = models.Manager()

    class Meta:
        abstract = True
        # ordering = ['-updated_at', '-created_at']
        ordering = ['-created_at']

    def delete(self, **kwargs):
        self.deleted_status = True
        self.deleted_at = timezone.now()
        self.save()


class StoreType(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="類型名稱")
    icon = models.CharField(max_length=128, help_text="標籤名稱")

    class Meta:
        ordering = ['created_at']


class County(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="縣市名稱")
    picture = models.CharField(max_length=128, help_text="縣市圖片")


class District(DefaultAbstract):
    county = models.ForeignKey(County, related_name="district", on_delete=models.CASCADE, help_text="縣市fk")
    name = models.CharField(max_length=128, help_text="行政區名稱")


class Store(DefaultAbstract):
    name = models.CharField(max_length=64, help_text="商家名稱")
    store_type = models.ForeignKey(StoreType, related_name="store", on_delete=models.CASCADE, help_text="店家類型fk")
    phone = models.CharField(max_length=64, help_text="電話")
    person = models.CharField(max_length=64, help_text="聯絡人", null=True)
    email = models.CharField(max_length=64, help_text="信箱", null=True)
    website = models.CharField(max_length=64, null=True, blank=True, help_text="網站")
    address = models.CharField(max_length=64, help_text="商家地址")
    latitude = models.FloatField(max_length=64, help_text="經度")
    longitude = models.FloatField(max_length=64, help_text="緯度")
    county = models.ForeignKey(County, related_name="store", on_delete=models.CASCADE, help_text="縣市fk")
    district = models.ForeignKey(District, related_name="store", on_delete=models.CASCADE, help_text="行政區fk")
    status = models.SmallIntegerField(default=0, help_text="商家狀態 0：待審核；1：審核通過（上架）；2：審核失敗（不顯示）")


class DiscountType(DefaultAbstract):
    name = models.CharField(max_length=128, help_text="折扣名稱")


class StoreDiscount(DefaultAbstract):
    store = models.ForeignKey(Store, related_name="storediscount", on_delete=models.CASCADE, help_text="")
    discount_type = models.ForeignKey(DiscountType, related_name="store_discount", on_delete=models.CASCADE,
                                      help_text="折扣fk")
    name = models.CharField(max_length=128, help_text="折扣標題")
    description = models.CharField(max_length=128, help_text="敘述")


class StoreImage(DefaultAbstract):
    store = models.ForeignKey(Store, related_name="storeimage", on_delete=models.CASCADE, help_text="商家fk")
    picture = models.CharField(max_length=128, help_text="商家圖片")


class File(DefaultAbstract):
    file = models.FileField()
