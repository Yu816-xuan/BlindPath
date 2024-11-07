import json
from django.shortcuts import render, get_object_or_404
from .models import Monitor, Alarm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    monitors = Monitor.objects.all()
    monitor_id = request.GET.get('monitor_id')

    # 获取 `monitor_id`，如果没有在请求中提供，则使用第一个监控项的 ID
    if monitor_id:
        try:
            monitor = Monitor.objects.get(id=monitor_id)
        except Monitor.DoesNotExist:
            monitor = monitors.first()
    else:
        monitor = monitors.first()
        monitor_id = monitor.id  # 默认第一个监控项的 ID

    alarms = Alarm.objects.filter(monitor=monitor).order_by('-alarm_time')

    return render(request, 'myapp/home.html', {
        'monitors': monitors,
        'selected_monitor': monitor,
        'alarms': alarms,
        'monitor_id': monitor_id,  # 将 `monitor_id` 传递给模板
    })



def monitor_details(request, monitor_id):
    try:
        monitor = Monitor.objects.get(id=monitor_id)
    except Monitor.DoesNotExist:
        return JsonResponse({'error': 'Monitor not found'}, status=404)

    data = {
        "id": monitor.id,
        "location": monitor.location,
        "latitude": monitor.latitude,
        "longitude": monitor.longitude,
        "video_url": monitor.video_url,
    }
    return JsonResponse(data)

def get_alarms_for_monitor(request, monitor_id):
    alarms = Alarm.objects.filter(monitor_id=monitor_id).values('obstacle_type', 'alarm_time', 'is_processed')

    if not alarms:
        return JsonResponse({'error': 'No alarms found for this monitor'}, status=404)

    alarms_data = list(alarms)
    return JsonResponse({'alarms': alarms_data})

@csrf_exempt
def update_alarm_status(request, monitor_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')

            if status not in ['已处理', '未处理']:
                return JsonResponse({'success': False, 'message': '无效的状态'}, status=400)

            alarms = Alarm.objects.filter(monitor_id=monitor_id)
            if not alarms.exists():
                return JsonResponse({'success': False, 'message': '没有找到报警记录'}, status=404)

            for alarm in alarms:
                alarm.is_processed = (status == '已处理')
                alarm.save()

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': '请求体格式错误'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': '不支持的请求方式'}, status=405)

def monitoring_statistics(request):
    return render(request, 'myapp/monitoring_statistics.html')

def map_view(request):
    monitors = Monitor.objects.all()
    return render(request, 'map.html', {
        'monitors': monitors,
    })
