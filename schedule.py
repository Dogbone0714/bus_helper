from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime
# 時刻表
bus_schedule = {
    "二坪山": ["07:25","07:30","07:40","07:45","07:50","08:00","08:25","08:30","08:40","08:45","08:50","09:25","09:40","09:50","09:55","10:50","11:15","11:20","11:40","11:50","12:20","12:30","12:40","12:50","12:55","13:00","13:15","13:40","13:45","14:20","14:40","14:50","15:00","15:15",'15:30',"15:50","16:30","16:40","16:50","17:15","17:20","18:00","18:20","18:45","19:20","20:30","21:45"],
    "八甲": ["07:35", "07:40","07:50", "07:55", "08:00","08:05","08:35","08:40","08:50","09:00","09:35","09:45","10:00","10:50","11:20","11:45","12:05","12:10","12:30","12:40","12:50","13:00","13:05","13:30","13:45","13:50","14:20","14:30","14:50","15:00","15:20","15:40","15:45","16:20","16:40","17:10","17:15","17:30","18:10","18:30","19:30","20:40","21:55"]
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

# ====== LINE Bot 設定 ======
app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "eJgxRpW55jfERoBH9Dm4aK+vyMcLIBxlH2wcGxhNsNEd+UYYtMEp0hewFPRGbbz7Za2nN0j2sL5NZzeraKFcPjQXcx1ihbSl3iFFXOYjRxrXsPpi68uovdXjpyvWJLIU6UaymV89bwIojn2OJfoHnwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0b2f138bb8c972e2478f7cb697dcbca8"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/")
def home():
    return "聯大校車 LINE Bot 啟動中！"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()
    if user_message in bus_schedule:
        reply = next_bus(user_message)
    else:
        reply = "請輸入目的地名稱，例如：二坪山、八甲"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    app.run(debug=True)