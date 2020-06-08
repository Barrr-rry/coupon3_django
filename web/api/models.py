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


class Oil(DefaultAbstract):
    CPC_oil_92 = models.FloatField(help_text="中油:92", null=True)
    CPC_oil_95 = models.FloatField(help_text="中油:95", null=True)
    CPC_oil_98 = models.FloatField(help_text="中油:98", null=True)
    CPC_diesel_oil = models.FloatField(help_text="中油:柴油", null=True)

    FPC_oil_92 = models.FloatField(help_text="中台塑:92", null=True)
    FPC_oil_95 = models.FloatField(help_text="中台塑:95", null=True)
    FPC_oil_98 = models.FloatField(help_text="中台塑:98", null=True)
    FPC_diesel_oil = models.FloatField(help_text="台塑:柴油", null=True)
    announce_status = models.BooleanField(default=False, help_text="油價通知公告")
    diesel_change = models.FloatField(help_text="柴油上漲多少錢 if 負數 then 下跌", null=True)
    oil_change = models.FloatField(help_text="上漲多少錢 if 負數 then 下跌", null=True)
    last_updated_at = models.DateTimeField(null=True, help_text='最後更新時間（網頁）')


class Traffic(DefaultAbstract):
    data_type = models.CharField(max_length=256, help_text="種類 ex: 事故", null=True)
    region = models.CharField(max_length=256, help_text="區域 ex: 高雄支線-國道10號", null=True)
    subject = models.CharField(max_length=256, help_text="主題 ex: 中正一路和輔仁路交會路口 自小客與機車", null=True)
    from_created_at = models.DateTimeField(null=True, help_text='card 右邊的時間')
    from_edit_at = models.DateTimeField(null=True, help_text='card 左邊的時間')
    fake_id = models.CharField(max_length=256, help_text="主題 ex: 爬蟲抓到card 的id 如果重複抓就用更新的", unique=True)
    lat = models.FloatField(help_text="經度", null=True)
    long = models.FloatField(help_text="經度", null=True)
