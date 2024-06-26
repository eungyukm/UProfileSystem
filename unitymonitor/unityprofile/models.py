from django.db import models
from django.utils import timezone


class DeviceInfo(models.Model):
    device_idx = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=30, default='none', unique=True)
    device_profile_name = models.CharField(max_length=30, default='none')
    

# Create your models here.
class ProfileData(models.Model):
    profile_idx = models.AutoField(primary_key=True)
    profile_count = models.IntegerField(default="-1")
    device_name = models.CharField(max_length=100, default="none")
    project_name = models.CharField(max_length=100, default="none")
    scene_name = models.CharField(max_length=100, default="none")
    date_time = models.DateTimeField(auto_now_add=True)
    
    fps = models.FloatField(default=0.0)
    min_fps = models.FloatField(default=0.0)
    avg_fps = models.FloatField(default=0.0)
    max_fps = models.FloatField(default=0.0)
    set_pass_call = models.FloatField(default=0.0)
    draw_call = models.FloatField(default=0.0)
    tris = models.FloatField(default=0.0)
    vertices = models.FloatField(default=0.0)

    total_memory = models.FloatField(default=0.0)
    system_memory = models.FloatField(default=0.0)
    texture_memory = models.FloatField(default=0.0)
    mesh_memory = models.FloatField(default=0.0)

    user_nickname = models.CharField(max_length=100, default="none")
    build_version = models.CharField(max_length=100, default="none")
    system_os = models.CharField(max_length=100, default="none")

class ProfileRecordInfo(models.Model):
    profile_record_info_idx = models.AutoField(primary_key=True)
    profile_record_title = models.CharField(max_length=100, default="none")
    profile_record_contents = models.CharField(max_length=500, default="none")
    date_time = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, default="none")
    profile_record_start_idx = models.IntegerField(default="-1")
    profile_record_end_idx = models.IntegerField(default="-1")

class ProfileRecord(models.Model):
    profile_record_idx = models.AutoField(primary_key=True)
    profile_count = models.IntegerField(default="-1")
    device_name = models.CharField(max_length=100, default="none")
    project_name = models.CharField(max_length=100, default="none")
    scene_name = models.CharField(max_length=100, default="none")
    date_time = models.DateTimeField(auto_now_add=True)
    
    fps = models.FloatField(default=0.0)
    min_fps = models.FloatField(default=0.0)
    avg_fps = models.FloatField(default=0.0)
    max_fps = models.FloatField(default=0.0)
    set_pass_call = models.FloatField(default=0.0)
    draw_call = models.FloatField(default=0.0)
    tris = models.FloatField(default=0.0)
    vertices = models.FloatField(default=0.0)

    total_memory = models.FloatField(default=0.0)
    system_memory = models.FloatField(default=0.0)
    texture_memory = models.FloatField(default=0.0)
    mesh_memory = models.FloatField(default=0.0)

    user_nickname = models.CharField(max_length=100, default="none")
    build_version = models.CharField(max_length=100, default="none")
    system_os = models.CharField(max_length=100, default="none")

    profile_record_info = models.ForeignKey(ProfileRecordInfo, on_delete=models.CASCADE, related_name='record_infos')

class ProfileLiveData(models.Model):
    profile_live_data_id = models.AutoField(primary_key=True)
    profile_count = models.IntegerField(default="-1")
    device_name = models.CharField(max_length=100, default="none")
    project_name = models.CharField(max_length=100, default="none")
    scene_name = models.CharField(max_length=100, default="none")
    # date는 datetime으로 변경
    date_time = models.DateTimeField(auto_now_add=True)
    
    fps = models.FloatField(default=0.0)
    min_fps = models.FloatField(default=0.0)
    avg_fps = models.FloatField(default=0.0)
    max_fps = models.FloatField(default=0.0)
    set_pass_call = models.FloatField(default=0.0)
    draw_call = models.FloatField(default=0.0)
    tris = models.FloatField(default=0.0)
    vertices = models.FloatField(default=0.0)

    total_memory = models.FloatField(default=0.0)
    system_memory = models.FloatField(default=0.0)
    texture_memory = models.FloatField(default=0.0)
    mesh_memory = models.FloatField(default=0.0)

    user_nickname = models.CharField(max_length=100, default="none")
    build_version = models.CharField(max_length=100, default="none")
    system_os = models.CharField(max_length=100, default="none")
