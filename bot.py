# =====================================================
# الملف الرئيسي لتشغيل البوت
# =====================================================

import telebot
import threading
import time
from telebot import types
from settings import TOKEN, TEST_DURATION, GEMINI_API_KEY
from handlers.user_session import user_data, UserSession
from languages.translations import LANGUAGES, get_text
from keyboards.buttons import create_language_keyboard, create_start_keyboard
from handlers.sections import start_section_1, show_final_results
from handlers.answers import handle_answer, handle_voice, handle_writing

bot = telebot.TeleBot(TOKEN)

# =====================================================
# أوامر البوت الرئيسية
# =====================================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data[user_id] = UserSession(user_id)
    bot.send_message(
        user_id,
        "🌐 مرحباً بك في اختبار اللغة العربية!\n\n" + get_text(user_id, "choose_lang"),
        reply_markup=create_language_keyboard()
    )

@bot.message_handler(func=lambda message: message.text in LANGUAGES.values())
def handle_language_selection(message):
    user_id = message.from_user.id
    selected_lang = message.text
    
    for lang_key, lang_name in LANGUAGES.items():
        if lang_name == selected_lang:
            user_data[user_id].language = lang_key
            break
    
    session = user_data.get(user_id)
    if session:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(
            user_id,
            f"✅ تم اختيار اللغة: {selected_lang}\n\n" + get_text(user_id, "test_start"),
            reply_markup=markup
        )
        bot.send_message(user_id, get_text(user_id, "test_duration"))
        bot.send_message(user_id, get_text(user_id, "test_sections"))
        
        bot.send_message(
            user_id,
            get_text(user_id, "press_button"),
            reply_markup=create_start_keyboard(user_id)
        )

@bot.message_handler(func=lambda message: message.text == get_text(message.from_user.id, "press_button"))
def start_test(message):
    user_id = message.from_user.id
    session = user_data.get(user_id)
    
    if not session or session.is_finished:
        bot.send_message(user_id, get_text(user_id, "error"))
        return
    
    session.start_time = time.time()
    markup = types.ReplyKeyboardRemove()
    bot.send_message(user_id, "🚀 جاري بدء الاختبار...", reply_markup=markup)
    start_section_1(user_id, bot)
    check_time(user_id)

def check_time(user_id):
    session = user_data.get(user_id)
    if not session or session.is_finished:
        return
    
    elapsed = time.time() - session.start_time
    remaining = TEST_DURATION - elapsed
    
    if remaining <= 0:
        bot.send_message(user_id, get_text(user_id, "time_up"))
        show_final_results(user_id, bot)
        return
    
    # تذكير بالوقت كل 5 دقائق
    if int(remaining) % 300 < 60:
        minutes = int(remaining / 60)
        bot.send_message(user_id, f"⏰ الوقت المتبقي: {minutes} دقيقة")
    
    threading.Timer(60, check_time, args=[user_id]).start()

# =====================================================
# معالجة الرسائل والملفات
# =====================================================

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id
    session = user_data.get(user_id)
    
    if not session:
        return
    
    if message.text in LANGUAGES.values() or message.text == get_text(user_id, "press_button"):
        return
    
    if session.waiting_for_writing:
        handle_writing(user_id, message.text, bot)
        return
    
    if session.waiting_for_answer:
        handle_answer(user_id, message.text, bot)
        return

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    user_id = message.from_user.id
    session = user_data.get(user_id)
    
    if not session:
        return
    
    if session.waiting_for_voice:
        handle_voice(user_id, message.voice, bot)
    else:
        bot.send_message(user_id, get_text(user_id, "error"))

@bot.message_handler(content_types=['audio', 'document'])
def handle_other_files(message):
    bot.send_message(message.from_user.id, get_text(message.from_user.id, "error"))

# =====================================================
# تشغيل البوت
# =====================================================

if __name__ == "__main__":
    print("🤖 البوت يعمل الآن مع Gemini API...")
    print(f"📝 التوكن: {TOKEN[:10]}...")
    print(f"🔑 مفتاح Gemini: {'موجود' if GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY_HERE' else 'غير موجود'}")
    try:
        bot.remove_webhook()
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ خطأ: {e}")
