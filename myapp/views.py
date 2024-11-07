from django.shortcuts import render
from .models import Monitor, Alarm

def home(request):
    monitors = Monitor.objects.all()
    # 默认选择第一个监控区域（如果用户没有选择）
    monitor_id = request.GET.get('monitor_id')
    if monitor_id:
        monitor = Monitor.objects.get(id=monitor_id)
    else:
        monitor = monitors.first()

    # 获取该监控区域的报警记录
    alarms = Alarm.objects.filter(monitor=monitor).order_by('-alarm_time')

    return render(request, 'myapp/home.html', {
        'monitors': monitors,
        'selected_monitor': monitor,
        'alarms': alarms,
    })

def monitoring_statistics(request):
    # 实时数据展示和统计图表
    return render(request, 'myapp/monitoring_statistics.html')

# 显示地图和监控报警信息
def map_view(request):
    # 获取所有监控区域
    monitors = Monitor.objects.all()

    return render(request, 'map.html', {
        'monitors': monitors,
    })
