import os
import random
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# إعداد المتغيرات والبيئة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

app_fastapi = FastAPI()
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

# تخزين جلسات المستخدمين
user_sessions = {}

# النماذج الثابتة باختيار من متعدد بالكامل وتضمين الروابط المباشرة
TEST_MODELS = [
    {
        "id": 1,
        "listening_link": "https://drive.google.com/file/d/18Oz_4GuxbQZUUQueWHDOlvGeqKL29kR0/view?usp=drivesdk",
        "questions": [
            # المفردات والقواعد (5 أسئلة)
            {
                "q": "1. ذهبتُ إلى _______ ليلاً لأشترى طعاماً وعصيراً.",
                "options": ["أ) المكتبة", "ب) السوبرماركت", "ج) المدرسة", "د) المستشفى"],
                "correct": "ب"
            },
            {
                "q": "2. لم يُسافرْ محمدٌ إلى دبي، و_______ يُسافرْ خالدٌ.",
                "options": ["أ) أيضاَ", "ب) كذلكَ", "ج) كذلكمْ", "د) لا"],
                "correct": "ب"
            },
            {
                "q": "3. المعلمُ _______ الشرحَ للطالبِ بوضوحٍ تامٍّ.",
                "options": ["أ) يشرَحُ", "ب) شَرَحَ", "ج) شارِحٌ", "د) مَشروحاتٌ"],
                "correct": "أ"
            },
            {
                "q": "4. ما هو جمع كلمة (كتاب)؟",
                "options": ["أ) كُتُبٌ", "ب) كِتاباتٌ", "ج) كاتِبونَ", "د) مَكتَباتٌ"],
                "correct": "أ"
            },
            {
                "q": "5. أيٌّ من الجمل الآتية صحيحة نحوياً وإملائياً؟",
                "options": ["أ) جاءَ الطلابُ جميعاً.", "ب) رأيتُ الطلابَ جميعاً.", "ج) مررتُ بالطلابِ جميعاً.", "د) جميع ما ذكر صحيح."],
                "correct": "د"
            },
            # القراءة (3 أسئلة)
            {
                "q": "6. (قراءة) «يُعتبرُ التراثُ الثقافيُّ لأي أمة هو المرآة التي تعكس هويتها وتاريخها...»\nماذا يُعتبر التراث الثقافي لأي أمة بحسب النص؟",
                "options": ["أ) مصدراً للدخل المؤقت فقط", "ب) المرآة التي تعكس الهوية والتاريخ العريق", "ج) عائقاً أمام التطور العمراني", "د) مكاناً ترفيهياً خالياً من التاريخ"],
                "correct": "ب"
            },
            {
                "q": "7. (قراءة) كيف تنشط المدن التاريخية الاقتصاد المحلي؟",
                "options": ["أ) عن طريق جذب السياح لمشاهدة المعالم القديمة", "ب) عن طريق بناء المصانع الحديثة", "ج) عن طريق إغلاقها أمام الزوار", "د) عن طريق فرض ضرائب عالية"],
                "correct": "أ"
            },
            {
                "q": "8. (قراءة) ما هو الشرط الأساسي الذي ذكره النص لحماية المواقع التاريخية؟",
                "options": ["أ) منع السياح نهائياً", "ب) تحويلها لمبانٍ سكنية", "ج) الحفاظ عليها من التلوث والتلف", "د) إزالة المعالم القديمة"],
                "correct": "ج"
            },
            # الاستماع (سؤال واحد)
            {
                "q": "9. (استماع) بعد الاستماع للملف الصوتي الأول، ما هي الفكرة الرئيسية التي ركز عليها النص؟",
                "options": ["أ) صعوبة تعلم قواعد اللغة العربية", "ب) أهمية تعلم لغات جديدة وأهمية العربية وضرورة الاستماع للطلاقة", "ج) تاريخ القرآن الكريم وتفسير آياته", "د) طرق السفر والسياحة حول العالم"],
                "correct": "ب"
            }
        ]
    },
    {
        "id": 2,
        "listening_link": "https://drive.google.com/file/d/16DyfOmABWymeDgFSCn7ux6reDKKnpR2O/view?usp=drivesdk",
        "questions": [
            # المفردات والقواعد (5 أسئلة)
            {
                "q": "1. سافر أخي إلى العاصمة _______ ليتعلم اللغة ويحصل على شهادة جامعية.",
                "options": ["أ) القاهرة", "ب) الجري", "ج) الكرسي", "د) الطاولة"],
                "correct": "أ"
            },
            {
                "q": "2. لم يكنِ الطالبُ كسولاً، بل كانَ _______ في دراسته.",
                "options": ["أ) مُجتهداً", "ب) مُجتهدٌ", "ج) مُجتهداًً", "د) مُجتهدٍ"],
                "correct": "أ"
            },
            {
                "q": "3. المعلمون _______ في إعداد المناهج الدراسية بعناية فائقة.",
                "options": ["أ) مُشارِكونَ", "ب) مُشارِكينَ", "ج) مُشارِكاتٌ", "د) مُشارِكاً"],
                "correct": "أ"
            },
            {
                "q": "4. ما هو ضد كلمة (واسع) في اللغة العربية؟",
                "options": ["أ) كبير", "ب) ضيق", "ج) طويل", "د) عميق"],
                "correct": "ب"
            },
            {
                "q": "5. أي من الكلمات الآتية تُعد ظرف مكان؟",
                "options": ["أ) أمس", "ب) فوق", "ج) سريعاً", "د) صباحاً"],
                "correct": "ب"
            },
            # القراءة (3 أسئلة)
            {
                "q": "6. (قراءة) «تُعتبر البيئة النظيفة حقاً أساسياً من حقوق الإنسان، ومسؤوليةً جماعيةً...»\nعلى من تقع مسؤولية الحفاظ على البيئة النظيفة بحسب النص؟",
                "options": ["أ) على الحكومات وحدها فقط", "ب) على الشركات الصناعية الكبرى", "ج) مسؤولية جماعية لا تقتصر على الحكومات وحدها", "د) على الأجيال القادمة فقط"],
                "correct": "ج"
            },
            {
                "q": "7. (قراءة) اذكر إحدى الخطوات الجوهرية التي ذكرها النص لبناء مستقبل مستدام:",
                "options": ["أ) زيادة استخدام البلاستيك", "ب) انتشار الأساليب الخضراء وإعادة التدوير", "ج) إيقاف وسائل النقل العامة", "د) بناء مصانع تقليدية"],
                "correct": "ب"
            },
            {
                "q": "8. (قراءة) ما هو الهدف الرئيسي من تقليل استخدام البلاستيك وحماية البيئة؟",
                "options": ["أ) بناء مستقبل مستدام وحماية كوكب الأرض من التغيرات المناخية", "ب) توفير الأموال للحكومات فقط", "ج) تقليل سرعة الرياح", "د) زيادة درجات الحرارة"],
                "correct": "أ"
            },
            # الاستماع (سؤال واحد)
            {
                "q": "9. (استماع) بعد الاستماع للملف الصوتي الثاني، ما هي الفكرة الأساسية التي ركز عليها النص؟",
                "options": ["أ) أهمية شراء جدول ورقي يومي", "ب) أهمية إدارة الوقت وتجنب التسويف وتنظيم المهام للإنتاج دون ضغط", "ج) طرق البحث العلمي الحديثة", "د) كيفية زيادة ساعات النوم"],
                "correct": "ب"
            }
        ]
    }
]

@app_fastapi.on_event("startup")
async def startup_event():
    await telegram_app.initialize()
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"
        await telegram_app.bot.set_webhook(url=webhook_url)

@app_fastapi.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🚀 ابدأ اختبار تحديد المستوى", callback_data="start_test")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في منصة اختبارات تحديد المستوى للغة العربية 🌐.\n"
        "الاختبار مكون من 9 أسئلة شاملة (مفردات، قواعد، قراءة، واستماع عبر جوجل درايف) وبدون ذكاء اصطناعي.",
        reply_markup=reply_markup
    )

async def start_test_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    # اختيار نموذج عشوائي (1 أو 2)
    selected_model = random.choice(TEST_MODELS)
    
    user_sessions[user_id] = {
        "model": selected_model,
        "current_q_index": 0,
        "score": 0
    }
    
    await send_next_question(query.message, user_id, edit=True)

async def send_next_question(message, user_id, edit=False):
    session = user_sessions[user_id]
    model = session["model"]
    index = session["current_q_index"]
    
    if index == 8:  # الوصول لسؤال الاستماع (السؤال التاسع)
        audio_link = model["listening_link"]
        await message.reply_text(
            "🎧 **مرحلة الاستماع:**\n"
            "الرجاء الاستماع للملف الصوتي عبر الرابط التالي أولاً:\n"
            f"🔗 [اضغط هنا لفتح ملف الاستماع]({audio_link})\n\n"
            "ثم أجب عن السؤال الأخير أدناه:"
        )

    q_data = model["questions"][index]
    
    keyboard = []
    for option in q_data["options"]:
        # استخراج الحرف الأول من الخيار مثل (أ، ب، ج، د)
        opt_letter = option.split(")")[0].strip()
        keyboard.append([InlineKeyboardButton(option, callback_data=f"ans_{opt_letter}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"📋 **سؤال ({index + 1}/9):**\n\n{q_data['q']}"
    
    if edit:
        await message.edit_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        await message.reply_text(text=text, reply_markup=reply_markup, disable_web_page_preview=True)

async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_sessions:
        await query.edit_message_text(text="انتهت الجلسة. الرجاء البدء مجدداً بـ /start")
        return

    selected_option = query.data.split("_")[1]
    session = user_sessions[user_id]
    model = session["model"]
    index = session["current_q_index"]
    
    correct_option = model["questions"][index]["correct"]
    
    # حساب الدرجة (كل سؤال عليه 11.1 درجة تقريباً لتكتمل من 100)
    if selected_option == correct_option:
        session["score"] += 11.1
    
    session["current_q_index"] += 1
    
    if session["current_q_index"] < len(model["questions"]):
        await send_next_question(query.message, user_id, edit=True)
    else:
        # انتهى الاختبار وحساب النتيجة والمستوى
        final_score = min(round(session["score"]), 100)
        
        if final_score <= 44:
            level = "A1 (مبتدئ)"
        elif final_score <= 65:
            level = "A2 (متوسط أدنى)"
        elif final_score <= 85:
            level = "B1 (متوسط)"
        else:
            level = "B2 (متقدم)"
            
        await query.edit_message_text(
            f"🎉 **لقد أنهيت الاختبار بنجاح!**\n\n"
            f"📊 درجتك النهائية: {final_score} / 100\n"
            f"🎯 مستواك اللغوي المحدد: **{level}**\n\n"
            "لإعادة الاختبار من جديد، اضغط على /start"
        )
        user_sessions.pop(user_id, None)

# تسجيل الهاندلرز في تطبيق تيليجرام
telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(CallbackQueryHandler(start_test_callback, pattern="^start_test$"))
telegram_app.add_handler(CallbackQueryHandler(answer_callback, pattern="^ans_"))

@app_fastapi.get("/")
def home():
    return {"status": "Arabic Level Assessment Bot with Fixed Links is running!"}
