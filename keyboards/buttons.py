# =====================================================
# أزرار البوت
# =====================================================

from telebot import types
from languages.translations import LANGUAGES, get_text

def create_language_keyboard():
    """إنشاء أزرار اختيار اللغة"""
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []
    for lang_key, lang_name in LANGUAGES.items():
        buttons.append(types.KeyboardButton(lang_name))
    markup.add(*buttons)
    return markup

def create_start_keyboard(user_id):
    """إنشاء زر بدء الاختبار"""
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton(get_text(user_id, "press_button")))
    return markup

def create_options_keyboard(options):
    """إنشاء أزرار الخيارات للإجابة"""
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for option in options:
        markup.add(types.KeyboardButton(option))
    return markup
