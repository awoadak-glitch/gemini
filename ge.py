import telebot
from google import genai

# الإعدادات (المفاتيح التي قدمتها)
TELEGRAM_TOKEN = '8694792877:AAG14Y5i2owSkY_Elv5D81uJIkeWniKDBDc'
GEMINI_API_KEY = 'AIzaSyABZMq8soZFuB0esoKvfbyl9_hNY7qPfx4'

# تهيئة البوت والعميل
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# مخزن مؤقت للمحادثات للحفاظ على السياق (الذاكرة)
sessions = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    
    # إنشاء جلسة محادثة جديدة إذا لم تكن موجودة
    if user_id not in sessions:
        sessions[user_id] = client.chats.create(
            model="gemini-2.0-flash",
            config={
                "system_instruction": "أنت مساعد ذكي ومحترف، تجيب على الأسئلة بدقة واختصار وتدعم الأكواد البرمجية والحلول التقنية."
            }
        )

    try:
        # إرسال رسالة المستخدم إلى Gemini
        response = sessions[user_id].send_message(message.text)
        
        # إرسال رد الذكاء الاصطناعي للمستخدم
        bot.reply_to(message, response.text, parse_mode='Markdown')
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ حدث خطأ أثناء الاتصال بـ Gemini، تأكد من صلاحية المفتاح.")

print("✅ بوت Gemini فعال الآن على التلجرام...")
bot.infinity_polling()
