import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

DB_PATH = "customer_service.db"

app = FastAPI()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


def save_line_message(user_id, text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS line_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        message TEXT,
        created_at TEXT
    )
    """)

    c.execute("""
    INSERT INTO line_messages (user_id, message, created_at)
    VALUES (?, ?, ?)
    """, (
        user_id,
        text,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def simple_reply(text):
    if "電力" in text or "跳電" in text:
        return "已收到電力相關問題，請確認斷路器、保險絲、電壓、PLC 或變頻器警報碼。"

    if "水" in text or "泵浦" in text:
        return "已收到水務相關問題，請確認水壓、水位、泵浦、閥件與管線狀態。"

    if "馬達" in text or "異音" in text or "卡住" in text:
        return "已收到機構相關問題，請確認馬達、軸承、皮帶、傳動件與潤滑狀態。"

    return "已收到您的問題，客服系統已記錄。若有警報碼或照片，請一併提供。"


@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature")
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    user_id = event.source.user_id

    save_line_message(user_id, user_text)

    reply = simple_reply(user_text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )
