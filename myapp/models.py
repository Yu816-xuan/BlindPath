from django.db import models

# 监控区域
class Monitor(models.Model):
    location = models.CharField(max_length=255)  # 监控位置
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)  # 纬度
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)  # 经度
    video_url = models.URLField(max_length=200, blank=True, null=True)  # 视频 URL

    def __str__(self):
        return self.location

    @property
    def alarms(self):
        return self.alarm_set.all()

    class Meta:
        db_table = 'monitor'  # Ensure this matches the table name in the database


# 报警事件
class Alarm(models.Model):
    MONITOR_TYPE_CHOICES = [
        ('unknown', '未知'),
        ('vehicle', '车辆'),
        ('person', '行人'),
        ('other', '其他'),
    ]

    monitor = models.ForeignKey(Monitor, related_name='alarms', on_delete=models.CASCADE)  # 关联监控区域
    alarm_time = models.DateTimeField(auto_now_add=True)  # 报警时间
    obstacle_type = models.CharField(max_length=50, choices=MONITOR_TYPE_CHOICES, default='unknown')  # 障碍物类型
    is_processed = models.BooleanField(default=False)  # 是否处理
    notes = models.TextField(blank=True, null=True)  # 备注信息

    def __str__(self):
        return f"{self.alarm_time} - {self.monitor.location} - {self.obstacle_type}"
