# -*- coding: utf-8 -*-
import os, json, threading, time
from flask import Flask, request
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7145036494
CHANNEL_ID = None
CHANNEL_LINK = "https://t.me/+l20CWCyobz5mZDdk"

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)
os.makedirs("database", exist_ok=True)

def get_user(uid):
    p=f"database/{uid}.json"
    if os.path.exists(p):
        try:
            return json.load(open(p,encoding="utf-8"))
        except:
            pass
    return {"balance":0.0,"points":10,"hosts":0,"orders":0,"trial":False,"vip":False,"joined":datetime.now().isoformat()}

def save_user(uid,data):
    json.dump(data, open(f"database/{uid}.json","w",encoding="utf-8"), ensure_ascii=False)

def main_kb(uid):
    m=InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("\U0001f680 \u062e\u062f\u0645\u0627\u062a \u0627\u0644\u0633\u0648\u0634\u0627\u0644", callback_data="services"),
        InlineKeyboardButton("\U0001f5a5\ufe0f \u0627\u0644\u0627\u0633\u062a\u0636\u0627\u0641\u0627\u062a 24/7", callback_data="hosting"),
        InlineKeyboardButton("\U0001f4b0 \u0634\u062d\u0646 \u0627\u0644\u0631\u0635\u064a\u062f", callback_data="recharge"),
        InlineKeyboardButton("\U0001f464 \u062d\u0633\u0627\u0628\u064a", callback_data="profile")
    )
    if uid == ADMIN_ID:
        m.add(InlineKeyboardButton("\U0001f451 \u062a\u0642\u0631\u064a\u0631 \u0627\u0644\u0634\u0647\u0631 \U0001f504 (\u0644\u0644\u0623\u062f\u0645\u0646 \u0641\u0642\u0637)", callback_data="admin_month"))
    return m

def get_monthly_stats():
    total=len([f for f in os.listdir("database") if f.endswith(".json")])
    return total, datetime.now().strftime("%B %Y")

@bot.message_handler(commands=['start'])
def start_msg(message):
    uid=message.from_user.id
    user=get_user(uid)
    save_user(uid,user)
    welcome=f"\U0001f44b \u0623\u0647\u0644\u0627\u064b {message.from_user.first_name}\n\u2705 \u0627\u0644\u0628\u0648\u062a \u0634\u063a\u0627\u0644 24/7\n\U0001f4e2 \u0642\u0646\u0627\u062a\u0646\u0627: {CHANNEL_LINK}"
    bot.send_message(uid, welcome, reply_markup=main_kb(uid))

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid=call.from_user.id
    cid=call.message.chat.id
    d=call.data
    if d=="admin_month":
        if uid!=ADMIN_ID:
            bot.answer_callback_query(call.id, "\u0644\u0644\u0623\u062f\u0645\u0646 \u0641\u0642\u0637", show_alert=True)
            return
        total, month=get_monthly_stats()
        text=f"\U0001f451 \u062a\u0642\u0631\u064a\u0631 \u0634\u0647\u0631 {month}\n\n\U0001f465 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646: {total}\n\u2705 \u0627\u0644\u0628\u0648\u062a \u0634\u063a\u0627\u0644 24/7"
        m=InlineKeyboardMarkup()
        m.add(InlineKeyboardButton("\U0001f504 \u062a\u062d\u062f\u064a\u062b", callback_data="admin_month"))
        m.add(InlineKeyboardButton("\U0001f519 \u0631\u062c\u0648\u0639", callback_data="main"))
        bot.edit_message_text(text, cid, call.message.message_id, reply_markup=m)
        return
    bot.edit_message_text("\U0001f3e0 \u0627\u0644\u0631\u0626\u064a\u0633\u064a\u0629 - \u0634\u063a\u0627\u0644 24/7", cid, call.message.message_id, reply_markup=main_kb(uid))

def keep_alive():
    while True:
        time.sleep(500)
        print("Alive 24/7")

threading.Thread(target=keep_alive, daemon=True).start()

@app.route("/", methods=["GET","POST"])
def webhook():
    if request.method=="POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode("utf-8"))])
    return "Bot Live 24/7",200

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))