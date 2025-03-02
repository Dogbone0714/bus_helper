from datetime import datetime, timedelta

# 簡單示範的時刻表
bus_schedule = {
    "二坪山校區": ["08:00", "12:00", "16:30", "18:00"],
    "八甲校區": ["07:35", "07:40","07:50", "07:55", "08:00","08:05","08:35","08:40","08:50","09:00","09:35","09:45","10:00","10:50","11:20","11:45","12:05"]
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