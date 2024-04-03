from django.db import models


class DeviceInfo(models.Model):
    device_idx = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=30, default='none', unique=True)
    device_profile_name = models.CharField(max_length=30, default='none')

class DeviceInfo2(models.Model):
    device_idx = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=30, default='none', unique=True)
    device_profile_name = models.CharField(max_length=30, default='none')

class DeviceInfo3(models.Model):
    device_idx = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=30, default='none', unique=True)
    device_profile_name = models.CharField(max_length=30, default='none')