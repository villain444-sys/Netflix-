import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Yahan BotFather wala token dalo
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(BOT_TOKEN)

# User ka device choice save karne ke liye
user_choices = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    # 3 Buttons create kar rahe hain
    markup.add(
        InlineKeyboardButton("📱 MOBILE", callback_data="mobile"),
        InlineKeyboardButton("💻 PC/LAPTOP", callback_data="pc"),
        InlineKeyboardButton("📺 TV", callback_data="tv")
    )
    bot.send_message(message.chat.id, "Link kiske liye banvana hai? Niche click karo:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # User ne kya select kiya wo save kar lenge
    user_choices[call.message.chat.id] = call.data
    bot.send_message(call.message.chat.id, "Apna link send karo 🔗")

@bot.message_handler(func=lambda message: True)
def process_link(message):
    chat_id = message.chat.id
    
    # Check karenge ki user ne button dabaya hai ya direct link bhej diya
    if chat_id not in user_choices:
        bot.send_message(chat_id, "Bhai pehle /start daal kar device select karo.")
        return

    original_link = message.text
    choice = user_choices[chat_id]
    new_link = original_link

    # Agar link me 'browse' word hai tabhi replace karega
    if "browse" in original_link:
        if choice == "mobile":
            new_link = original_link.replace("browse", "unsupported")
        elif choice == "pc":
            new_link = original_link.replace("browse", "browse") 
        elif choice == "tv":
            new_link = original_link.replace("browse", "tv9")

        bot.send_message(chat_id, f"✅ Yeh raha tumhara modify kiya hua link:\n\n{new_link}")
        
        # Kaam hone ke baad data clear kar do taaki agle link ke liye wapas button dabana pade
        del user_choices[chat_id]
    else:
        bot.send_message(chat_id, "❌ Is link me 'browse' word nahi hai. Netflix ka sahi token link bhejo.")

# Bot ko 24/7 on rakhne ke liye
print("Bot chalu ho gaya hai...")
bot.infinity_polling()
  
