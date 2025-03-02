from datetime import datetime, timedelta

# 時刻表
bus_schedule = {
    "二坪山校區": ["07:25","07:30","07:40","07:45","07:50","08:00","08:25","08:30","08:40","08:45","08:50","09:25","09:40","09:50","09:55","10:50","11:15","11:20","11:40","11:50","12:20","12:30","12:40","12:50","12:55","13:00",""],
    "八甲校區": ["07:35", "07:40","07:50", "07:55", "08:00","08:05","08:35","08:40","08:50","09:00","09:35","09:45","10:00","10:50","11:20","11:45","12:05","12:10","12:30","12:40","12:50","13:00","13:05","13:30","13:45","13:50","14:20","14:30","14:50","15:00","15:20","15:40","15:45","16:20","16:40","17:10","17:15","17:30","18:10","18:30","19:30","20:40","21:55"]
}

def next_bus(destination):
    now = datetime.now()
    times = bus_schedule.get(destination, [])

    for time_str in times:
        bus_time = datetime.strptime(time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if bus_time > now:
            remaining = bus_time - now
            return f"下一班往 {destination} 的校車是 {time_str}，剩餘 {remaining.seconds // 60} 分鐘。"
    return f"今天往 {destination} 的校車已經沒了！"