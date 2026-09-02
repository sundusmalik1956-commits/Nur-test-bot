import os
import random
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

app = FastAPI()
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

user_sessions = {}

UI_TEXTS = {
    "ar": {
        "welcome": "أهلاً بك في منصة اختبارات تحديد المستوى للغة العربية.\nالرجاء اختيار لغة الواجهة والتعليمات:",
        "start_btn": "بدء الاختبار",
        "audio_intro": "🎧 وصلْتَ إلى قسم الاستماع الأخير. استمع للملف الصوتي أولاً ثم اضغط على الزر أدناه للإجابة:",
        "answer_btn": "الإجابة على السؤال",
        "question_title": "سؤال",
        "finished": "لقد أنهيت الاختبار بنجاح!",
        "score_label": "درجتك النهائية",
        "level_label": "مستواك اللغوي المحدد",
        "restart": "لإعادة الاختبار من جديد، اضغط على امر البدء /start",
        "session_expired": "انتهت الجلسة. الرجاء البدء مجدداً بـ /start"
    },
    "tr": {
        "welcome": "Arapça seviye tespiti test platformuna hoş geldiniz.\nLütfen arayüz ve talimat dilini seçin:",
        "start_btn": "Testi Başlat",
        "audio_intro": "🎧 Dinleme bölümüne geldiniz. Önce ses dosyasını dinleyin, ardından soruyu yanıtlamak için aşağıdaki düğmeye tıklayın:",
        "answer_btn": "Soruyu Cevapla",
        "question_title": "Soru",
        "finished": "Testi başarıyla tamamladınız!",
        "score_label": "Final puanınız",
        "level_label": "Belirlenen dil seviyeniz",
        "restart": "Testi yeniden başlatmak için /start komutunu kullanın",
        "session_expired": "Oturum süresi doldu. Lütfen /start ile tekrar başlayın"
    },
    "en": {
        "welcome": "Welcome to the Arabic language placement test platform.\nPlease choose the interface and instructions language:",
        "start_btn": "Start Test",
        "audio_intro": "🎧 You have reached the listening section. Listen to the audio file first, then click the button below to answer:",
        "answer_btn": "Answer Question",
        "question_title": "Question",
        "finished": "You have successfully finished the test!",
        "score_label": "Your final score",
        "level_label": "Your determined language level",
        "restart": "To retake the test, press /start",
        "session_expired": "Session expired. Please start with /start"
    },
    "fr": {
        "welcome": "Bienvenue sur la plateforme de test de niveau de langue arabe.\nVeuillez choisir la langue de l'interface et des instructions:",
        "start_btn": "Commencer le test",
        "audio_intro": "🎧 Vous êtes arrivé à la section d'écoute. Écoutez le fichier audio puis cliquez ci-dessous pour répondre :",
        "answer_btn": "Répondre à la question",
        "question_title": "Question",
        "finished": "Vous avez terminé le test avec succès!",
        "score_label": "Votre score final",
        "level_label": "Votre niveau de langue déterminé",
        "restart": "Pour refaire le test, appuyez sur /start",
        "session_expired": "Session expirée. Veuillez recommencer avec /start"
    },
    "de": {
        "welcome": "Willkommen auf der Einstufungstest-Plattform für die arabische Sprache.\nBitte wählen Sie die Sprach- und Anweisungssprache:",
        "start_btn": "Test starten",
        "audio_intro": "🎧 Sie haben den Hörbereich erreicht. Hören Sie sich zuerst die Audiodatei an und klicken Sie unten, um zu antworten:",
        "answer_btn": "Frage beantworten",
        "question_title": "Frage",
        "finished": "Sie haben den Test erfolgreich beendet!",
        "score_label": "Ihre Endpunktzahl",
        "level_label": "Ihr ermitteltes Sprachniveau",
        "restart": "Um den Test zu wiederholen, tippen Sie auf /start",
        "session_expired": "Sitzung abgelaufen. Bitte starten Sie mit /start"
    },
    "es": {
        "welcome": "Bienvenido a la plataforma de prueba de nivel de idioma árabe.\nPor favor, elija el idioma de la interfaz y las instrucciones:",
        "start_btn": "Comenzar prueba",
        "audio_intro": "🎧 Has llegado a la sección de escucha. Escucha el archivo de audio y haz clic abajo para responder:",
        "answer_btn": "Responder pregunta",
        "question_title": "Pregunta",
        "finished": "¡Has terminado la prueba con éxito!",
        "score_label": "Tu puntuación final",
        "level_label": "Tu nivel de idioma determinado",
        "restart": "Para repetir la prueba, presiona /start",
        "session_expired": "Sesión caducada. Por favor comienza con /start"
    },
    "ru": {
        "welcome": "Добро пожаловать на платформу тестирования уровня арабского языка.\nПожалуйста, выберите язык интерфейса и инструкций:",
        "start_btn": "Начать тест",
        "audio_intro": "🎧 Вы перешли к разделу аудирования. Прослушайте аудиофайл и нажмите кнопку ниже, чтобы ответить:",
        "answer_btn": "Ответить на вопрос",
        "question_title": "Вопрос",
        "finished": "Вы успешно завершили тест!",
        "score_label": "Ваш итоговый балл",
        "level_label": "Ваш определенный уровень языка",
        "restart": "Чтобы пройти тест заново, нажмите /start",
        "session_expired": "Сессия истекла. Начните заново с /start"
    },
    "zh": {
        "welcome": "欢迎来到阿拉伯语水平测试平台。\n请选择界面和说明语言：",
        "start_btn": "开始测试",
        "audio_intro": "🎧 您已到达听力部分。请先听音频文件，然后点击下方按钮回答：",
        "answer_btn": "回答问题",
        "question_title": "问题",
        "finished": "您已成功完成测试！",
        "score_label": "您的最终得分",
        "level_label": "您确定的语言水平",
        "restart": "要重新测试，请按 /start",
        "session_expired": "会话已过期，请使用 /start 重新开始"
    },
    "ja": {
        "welcome": "アラビア語レベルテストプラットフォームへようこそ。\nインターフェースと説明の言語を選択してください：",
        "start_btn": "テストを開始",
        "audio_intro": "🎧 リスニングセクションに到達しました。音声ファイルを聞いてから、下のボタンを押して回答してください：",
        "answer_btn": "質問に答える",
        "question_title": "質問",
        "finished": "テストが正常に終了しました！",
        "score_label": "最終スコア",
        "level_label": "判定された言語レベル",
        "restart": "もう一度テストを受けるには /start を押してください",
        "session_expired": "セッションの有効期限が切れました。/start から始めてください"
    }
}

TEST_MODELS = [
    {
        "id": 1,
        "listening_audio_url": "https://drive.google.com/uc?export=download&id=18Oz_4GuxbQZUUQueWHDOlvGeqKL29kR0",
        "questions": [
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
            {
                "q": "6. (قراءة) «يُعتبرُ التراثُ الثقافيُّ لأي أمة هو المرآة التي تعكس هويتها وتاريخها العريق...»\nماذا يُعتبر التراث الثقافي لأي أمة بحسب النص؟",
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
            {
                "q": "9. (استماع) بعد الاستماع للملف الصوتي، ما هي الفكرة الرئيسية التي ركز عليها النص؟",
                "options": ["أ) صعوبة تعلم قواعد اللغة العربية", "ب) أهمية تعلم لغات جديدة وأهمية العربية وضرورة الاستماع للطلاقة", "ج) تاريخ القرآن الكريم وتفسير آياته", "د) طرق السفر والسياحة حول العالم"],
                "correct": "ب"
            }
        ]
    },
    {
        "id": 2,
        "listening_audio_url": "https://drive.google.com/uc?export=download&id=16DyfOmABWymeDgFSCn7ux6reDKKnpR2O",
        "questions": [
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
            {
                "q": "9. (استماع) بعد الاستماع للملف الصوتي، ما هي الفكرة الأساسية التي ركز عليها النص؟",
                "options": ["أ) أهمية شراء جدول ورقي يومي", "ب) أهمية إدارة الوقت وتجنب التسويف وتنظيم المهام للإنتاج دون ضغط", "ج) طرق البحث العلمي الحديثة", "د) كيفية زيادة ساعات النوم"],
                "correct": "ب"
            }
        ]
    }
]

@app.on_event("startup")
async def startup_event():
    await telegram_app.initialize()
    if RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}/webhook"
        await telegram_app.bot.set_webhook(url=webhook_url)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("العربية (Arabic)", callback_data="lang_ar"), InlineKeyboardButton("Türkçe (Turkish)", callback_data="lang_tr")],
        [InlineKeyboardButton("English", callback_data="lang_en"), InlineKeyboardButton("Français (French)", callback_data="lang_fr")],
        [InlineKeyboardButton("Deutsch (German)", callback_data="lang_de"), InlineKeyboardButton("Español (Spanish)", callback_data="lang_es")],
        [InlineKeyboardButton("Русский (Russian)", callback_data="lang_ru"), InlineKeyboardButton("中文 (Chinese)", callback_data="lang_zh")],
        [InlineKeyboardButton("日本語 (Japanese)", callback_data="lang_ja")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "اختر لغة الواجهة والتعليمات المفضلة لديك:\n"
        "Please choose your preferred interface language:\n"
        "Lütfen tercih ettiğiniz arayüz dilini seçin:",
        reply_markup=reply_markup
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = query.data.split("_")[1]
    
    user_sessions[user_id] = {
        "lang": lang,
        "current_q_index": 0,
        "score": 0
    }
    
    texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
    keyboard = [[InlineKeyboardButton(texts["start_btn"], callback_data="start_test")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(text=texts["welcome"], reply_markup=reply_markup)

async def start_test_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {"lang": "en", "current_q_index": 0, "score": 0}
        
    selected_model = random.choice(TEST_MODELS)
    user_sessions[user_id]["model"] = selected_model
    user_sessions[user_id]["current_q_index"] = 0
    user_sessions[user_id]["score"] = 0
    
    await send_current_step(query.message, user_id, edit=False, context=context)

async def send_current_step(message, user_id, edit=False, context=None):
    session = user_sessions[user_id]
    model = session["model"]
    index = session["current_q_index"]
    lang = session["lang"]
    texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
    
    # إذا كان السؤال التاسع، نرسل الصوت في رسالة مستقلة أولاً مع زر للانتقال للخيارات
    if index == 8:
        audio_url = model["listening_audio_url"]
        if edit:
            try:
                await message.delete()
            except Exception:
                pass
        
        keyboard = [[InlineKeyboardButton(texts["answer_btn"], callback_data="show_audio_question")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_audio(chat_id=user_id, audio=audio_url)
        await context.bot.send_message(chat_id=user_id, text=texts["audio_intro"], reply_markup=reply_markup)
        return

    q_data = model["questions"][index]
    keyboard = []
    for option in q_data["options"]:
        opt_letter = option.split(")")[0].strip()
        keyboard.append([InlineKeyboardButton(option, callback_data=f"ans_{opt_letter}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"{texts['question_title']} ({index + 1}/9):\n\n{q_data['q']}"
    
    if edit:
        try:
            await message.edit_text(text=text, reply_markup=reply_markup)
        except Exception:
            await message.reply_text(text=text, reply_markup=reply_markup)
    else:
        await message.reply_text(text=text, reply_markup=reply_markup)

async def show_audio_question_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_sessions:
        await query.message.reply_text("Session expired. Please start with /start")
        return
        
    session = user_sessions[user_id]
    model = session["model"]
    index = session["current_q_index"]
    lang = session["lang"]
    texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
    
    q_data = model["questions"][index]
    keyboard = []
    for option in q_data["options"]:
        opt_letter = option.split(")")[0].strip()
        keyboard.append([InlineKeyboardButton(option, callback_data=f"ans_{opt_letter}")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = f"{texts['question_title']} ({index + 1}/9):\n\n{q_data['q']}"
    await query.message.edit_text(text=text, reply_markup=reply_markup)

async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_sessions:
        lang = "ar"
        texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
        await query.message.reply_text(texts["session_expired"])
        return

    selected_option = query.data.split("_")[1]
    session = user_sessions[user_id]
    model = session["model"]
    index = session["current_q_index"]
    lang = session["lang"]
    texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
    
    correct_option = model["questions"][index]["correct"]
    
    if selected_option == correct_option:
        session["score"] += 11.1
    
    session["current_q_index"] += 1
    
    if session["current_q_index"] < len(model["questions"]):
        await send_current_step(query.message, user_id, edit=True, context=context)
    else:
        final_score = min(round(session["score"]), 100)
        
        if final_score <= 44:
            level = "A1"
        elif final_score <= 65:
            level = "A2"
        elif final_score <= 85:
            level = "B1"
        else:
            level = "B2"
            
        await query.message.edit_text(
            f"{texts['finished']}\n\n"
            f"{texts['score_label']}: {final_score} / 100\n"
            f"{texts['level_label']}: {level}\n\n"
            f"{texts['restart']}"
        )
        user_sessions.pop(user_id, None)

telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
telegram_app.add_handler(CallbackQueryHandler(start_test_callback, pattern="^start_test$"))
telegram_app.add_handler(CallbackQueryHandler(show_audio_question_callback, pattern="^show_audio_question$"))
telegram_app.add_handler(CallbackQueryHandler(answer_callback, pattern="^ans_"))

@app.get("/")
def home():
    return {"status": "Arabic Level Assessment Bot is running smoothly!"}
