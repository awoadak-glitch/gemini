import telebot
from google import genai
import os
import time

# سحب المفاتيح من بيئة العمل (GitHub Secrets)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

sessions = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_id not in sessions:
        try:
            # استخدام الموديل الأكثر استقراراً
            sessions[user_id] = client.chats.create(model="gemini-1.5-flash")
        except Exception as e:
            bot.reply_to(message, "⚠️ فشل في تهيئة الموديل. تأكد من تفعيل المفتاح.")
            return

    try:
        response = sessions[user_id].send_message(message.text)
        bot.reply_to(message, response.text, parse_mode='Markdown')
    except Exception as e:
        # طباعة الخطأ كاملاً في GitHub Logs لنعرف السبب بدقة
        print(f"FULL ERROR: {e}")
        bot.reply_to(message, "⚠️ حدث خطأ في الاتصال. جرب مرة أخرى.")

if __name__ == "__main__":
    print("🚀 البوت يعمل الآن...")
    bot.infinity_polling()
