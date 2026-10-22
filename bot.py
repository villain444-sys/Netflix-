import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import os

# Yahan BotFather wala token dalo
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

user_choices = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📱 MOBILE", callback_data="mobile"),
        InlineKeyboardButton("💻 PC/LAPTOP", callback_data="pc"),
        InlineKeyboardButton("📺 TV", callback_data="tv")
    )
    bot.send_message(message.chat.id, "Link kiske liye banvana hai? Niche click karo:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_choices[call.message.chat.id] = call.data
    bot.send_message(call.message.chat.id, "Apna link send karo 🔗")

@bot.message_handler(func=lambda message: True)
def process_link(message):
    chat_id = message.chat.id
    
    if chat_id not in user_choices:
        bot.send_message(chat_id, "Bhai pehle /start daal kar device select karo.")
        return

    original_link = message.text
    choice = user_choices[chat_id]
    new_link = original_link

    if "browse" in original_link:
        if choice == "mobile":
            new_link = original_link.replace("browse", "unsupported")
        elif choice == "pc":
            new_link = original_link.replace("browse", "browse") 
        elif choice == "tv":
            new_link = original_link.replace("browse", "tv9")

        bot.send_message(chat_id, f"✅ Yeh raha tumhara modify kiya hua link:\n\n{new_link}")
        del user_choices[chat_id]
    else:
        bot.send_message(chat_id, "❌ Is link me 'browse' word nahi hai. Netflix ka sahi token link bhejo.")

# --- FLASK SERVER SETUP ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running on Render!"

def run_flask():
    # Render khud PORT assign karta hai, by default 8080 le lega
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask ko alag thread me chala rahe hain taaki bot block na ho
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("Bot chalu ho gaya hai...")
    bot.infinity_polling()
    
