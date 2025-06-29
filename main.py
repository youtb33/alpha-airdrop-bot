import feedparser
import time
import os
import requests
from googletrans import Translator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RSS_URL = "https://www.binance.com/en/support/announcement/rss"

KEYWORDS = ["airdrop", "Alpha", "空投"]

sent_items = set()
translator = Translator()

def translate_text(text):
    try:
        return translator.translate(text, dest="zh-cn").text
    except Exception as e:
        return text

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def check_rss():
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries:
        if entry.id in sent_items:
            continue
        for kw in KEYWORDS:
            if kw.lower() in entry.title.lower():
                translated = translate_text(entry.title + "\n" + entry.link)
                send_telegram_message(f"🔔 <b>{entry.title}</b>\n{translated}\n{entry.link}")
                sent_items.add(entry.id)
                break

if __name__ == "__main__":
    send_telegram_message("🤖 Alpha 空投机器人已上线！")
    while True:
        check_rss()
        time.sleep(300)
