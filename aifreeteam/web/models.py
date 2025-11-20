from django.db import models
from datetime import datetime
# Create your models here.

class achievement(models.Model):
	year = models.PositiveIntegerField(default=9999)
	name = models.CharField('專案/競賽/課程名稱', max_length=256)
	award = models.CharField('名次/獎項', max_length=256, default='')


class contact_email(models.Model):
	contact_name = models.CharField('聯絡人', max_length=256)
	contact_need = models.CharField('需求', max_length=20)
	contact_phone = models.CharField('聯絡電話', max_length=64)
	contact_email = models.CharField('聯絡信箱', max_length=128)
	contact_message = models.CharField('聯絡訊息', max_length=1024)
	contact_date = models.DateTimeField(default=datetime.now, blank=True)

class collect_email(models.Model):
    email = models.CharField('聯絡信箱', max_length=128, primary_key=True)
    collect_date = models.DateTimeField(default=datetime.now, blank=True)
    is_subscribed = models.BooleanField(default=True)