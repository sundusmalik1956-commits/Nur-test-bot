# -*- coding: utf-8 -*-
"""
بوت تيليجرام لاختبار تحديد مستوى اللغة العربية.
يعمل عبر FastAPI + Webhooks + python-telegram-bot v20.x
"""

import logging
import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from questions_data import get_random_model, gdrive_direct_link
from scoring import calculate_score, determine_level, get_level_label, TOTAL_QUESTIONS
from translations import LANGUAGES, t

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ============================================================
# إعدادات البيئة
# ============================================================
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "")
WEBHOOK_PATH = "/webhook"

if not TELEGRAM_BOT_TOKEN:
    logger.warning("⚠️ لم يتم ضبط TELEGRAM_BOT_TOKEN في متغيرات البيئة!")

# ============================================================
# تخزين حالة المستخدمين في الذاكرة
# ============================================================
# user_data المدمجة مع Application تكفي، لكن نحتفظ بهيكل واضح هنا للرجوع إليه
# state = {
#   "lang": "ar",
#   "model": {...},
#   "current_q": 0,
#   "correct_count": 0,
# }

# ============================================================
# بناء تطبيق تيليجرام
# ============================================================
telegram_app: Application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()


# ------------------------------------------------------------
# أمر /start : عرض اختيار اللغة
# ------------------------------------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # إعادة تعيين كاملة عند كل /start

    buttons = []
    row = []
    for i, (code, label) in enumerate(LANGUAGES.items(), start=1):
        row.append(InlineKeyboardButton(label, callback_data=f"lang:{code}"))
        if i % 2 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    keyboard = InlineKeyboardMarkup(buttons)
    # رسالة الاختيار تُعرض بالعربية والإنجليزية معاً كبداية محايدة
    text = f"{t('choose_language', 'ar')}\n\n{t('choose_language', 'en')}"
    await update.message.reply_text(text, reply_markup=keyboard)


# ------------------------------------------------------------
# اختيار اللغة
# ------------------------------------------------------------
async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = query.data.split(":")[1]
    context.user_data["lang"] = lang_code

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t("start_test_button", lang_code), callback_data="begin_test")]]
    )
    await query.edit_message_text(
        t("welcome_instructions", lang_code),
        reply_markup=keyboard,
    )


# ------------------------------------------------------------
# بدء الاختبار: اختيار نموذج عشوائي وعرض السؤال الأول
# ------------------------------------------------------------
async def begin_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang", "en")
    model = get_random_model()

    context.user_data["model"] = model
    context.user_data["current_q"] = 0
    context.user_data["correct_count"] = 0

    await send_question(update, context, edit=True)


# ------------------------------------------------------------
# إرسال سؤال بحسب الفهرس الحالي في user_data
# ------------------------------------------------------------
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, edit: bool = False):
    lang_code = context.user_data.get("lang", "en")
    model = context.user_data["model"]
    q_index = context.user_data["current_q"]
    question = model["questions"][q_index]

    chat_id = update.effective_chat.id

    # سؤال الاستماع (التاسع) له سير عمل خاص
    if question["type"] == "listening":
        await send_listening_intro(update, context, question)
        return

    # بناء نص السؤال (مع نص القراءة إن وُجد)
    progress = t("question_progress", lang_code, current=q_index + 1, total=TOTAL_QUESTIONS)
    parts = [progress, ""]

    if question["type"] == "reading":
        parts.append(t("reading_passage_title", lang_code))
        parts.append(f"\n「{question['passage']}」\n")

    parts.append(question["text"])
    text = "\n".join(parts)

    # أزرار الخيارات (كل خيار بزر منفصل)
    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"ans:{i}")]
        for i, opt in enumerate(question["options"])
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if edit and update.callback_query:
        try:
            await update.callback_query.edit_message_text(text, reply_markup=keyboard)
            return
        except Exception:
            pass  # في حال فشل التعديل (مثلاً بعد إرسال صوت)، نرسل رسالة جديدة

    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


# ------------------------------------------------------------
# إرسال مقدمة سؤال الاستماع: الملف الصوتي + زر "الإجابة على السؤال"
# ------------------------------------------------------------
async def send_listening_intro(update: Update, context: ContextTypes.DEFAULT_TYPE, question: dict):
    lang_code = context.user_data.get("lang", "en")
    chat_id = update.effective_chat.id

    audio_sent = False

    # المحاولة الأولى (والأفضل): إرسال عبر file_id ثابت مرفوع مسبقاً على تيليجرام
    file_id = question.get("audio_file_id")
    if file_id:
        try:
            await context.bot.send_audio(chat_id=chat_id, audio=file_id)
            audio_sent = True
        except Exception as e:
            logger.warning(f"فشل إرسال send_audio عبر file_id: {e}")

    # محاولة احتياطية: رابط جوجل درايف المباشر (فقط إذا لم ينجح file_id)
    if not audio_sent:
        direct_link = gdrive_direct_link(question["audio_link"])
        try:
            await context.bot.send_audio(chat_id=chat_id, audio=direct_link)
            audio_sent = True
        except Exception as e:
            logger.warning(f"فشل إرسال send_audio بالرابط المباشر: {e}")
            try:
                async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
                    resp = await client.get(direct_link)
                    if resp.status_code == 200 and len(resp.content) > 1000:
                        await context.bot.send_audio(
                            chat_id=chat_id,
                            audio=resp.content,
                            filename="listening.mp3",
                        )
                        audio_sent = True
            except Exception as e2:
                logger.warning(f"فشل تحميل/إرسال الملف الصوتي يدوياً: {e2}")

    if not audio_sent:
        await context.bot.send_message(
            chat_id=chat_id,
            text=t("audio_send_error", lang_code, link=question["audio_link"]),
        )

    # رسالة الإرشاد + زر الإجابة على السؤال
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(t("answer_question_button", lang_code), callback_data="show_listening_q")]]
    )
    await context.bot.send_message(
        chat_id=chat_id,
        text=t("listening_intro", lang_code),
        reply_markup=keyboard,
    )


# ------------------------------------------------------------
# عرض سؤال الاستماع نفسه بعد الضغط على "الإجابة على السؤال"
# ------------------------------------------------------------
async def show_listening_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang", "en")
    model = context.user_data["model"]
    q_index = context.user_data["current_q"]
    question = model["questions"][q_index]

    progress = t("question_progress", lang_code, current=q_index + 1, total=TOTAL_QUESTIONS)
    text = f"{progress}\n\n{question['text']}"

    buttons = [
        [InlineKeyboardButton(opt, callback_data=f"ans:{i}")]
        for i, opt in enumerate(question["options"])
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(text, reply_markup=keyboard)


# ------------------------------------------------------------
# استقبال إجابة المستخدم على أي سؤال
# ------------------------------------------------------------
async def answer_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang_code = context.user_data.get("lang", "en")
    model = context.user_data.get("model")
    if model is None:
        # المستخدم لم يبدأ اختباراً بعد (حالة غير متوقعة) - نطلب /start
        await query.edit_message_text(t("choose_language", lang_code))
        return

    selected_index = int(query.data.split(":")[1])
    q_index = context.user_data["current_q"]
    question = model["questions"][q_index]

    is_correct = selected_index == question["correct_index"]
    if is_correct:
        context.user_data["correct_count"] += 1

    next_q_index = q_index + 1
    context.user_data["current_q"] = next_q_index

    if next_q_index >= len(model["questions"]):
        # انتهى الاختبار: عرض النتيجة
        await show_result(update, context)
    else:
        # الانتقال للسؤال التالي
        await send_question(update, context, edit=True)


# ------------------------------------------------------------
# عرض النتيجة النهائية
# ------------------------------------------------------------
async def show_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = context.user_data.get("lang", "en")
    correct_count = context.user_data.get("correct_count", 0)

    score = calculate_score(correct_count, TOTAL_QUESTIONS)
    level_code = determine_level(correct_count)
    level_label = get_level_label(level_code, lang_code)

    text = "\n\n".join(
        [
            t("result_title", lang_code),
            t("result_score", lang_code, score=score, correct=correct_count, total=TOTAL_QUESTIONS),
            t("result_level", lang_code, level=level_label),
            t("restart_hint", lang_code),
        ]
    )

    try:
        await update.callback_query.edit_message_text(text)
    except Exception:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# ============================================================
# تسجيل المعالجات (Handlers)
# ============================================================
telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(CallbackQueryHandler(language_selected, pattern=r"^lang:"))
telegram_app.add_handler(CallbackQueryHandler(begin_test, pattern=r"^begin_test$"))
telegram_app.add_handler(CallbackQueryHandler(show_listening_question, pattern=r"^show_listening_q$"))
telegram_app.add_handler(CallbackQueryHandler(answer_selected, pattern=r"^ans:"))


# ============================================================
# تطبيق FastAPI + إدارة دورة الحياة (Webhook setup/teardown)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    await telegram_app.initialize()
    await telegram_app.start()

    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}{WEBHOOK_PATH}"
        try:
            await telegram_app.bot.set_webhook(url=webhook_url)
            logger.info(f"✅ تم ضبط الـ Webhook على: {webhook_url}")
        except Exception as e:
            logger.error(f"❌ فشل ضبط الـ Webhook: {e}")
    else:
        logger.warning("⚠️ RENDER_EXTERNAL_URL غير مضبوط، لم يتم تفعيل الـ Webhook تلقائياً.")

    yield

    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Arabic Level Test Bot is running."}


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return Response(status_code=200)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
