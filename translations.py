# -*- coding: utf-8 -*-
"""
نصوص الواجهة بجميع اللغات المدعومة:
العربية (ar) - التركية (tr) - الإنجليزية (en) - الفرنسية (fr)
الألمانية (de) - الإسبانية (es) - الروسية (ru) - الصينية (zh) - اليابانية (ja)
"""

LANGUAGES = {
    "ar": "🇸🇦 العربية",
    "tr": "🇹🇷 Türkçe",
    "en": "🇬🇧 English",
    "fr": "🇫🇷 Français",
    "de": "🇩🇪 Deutsch",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
}

TEXTS = {
    "choose_language": {
        "ar": "🌍 مرحباً بك! الرجاء اختيار لغة الواجهة:",
        "tr": "🌍 Hoş geldiniz! Lütfen arayüz dilini seçin:",
        "en": "🌍 Welcome! Please choose the interface language:",
        "fr": "🌍 Bienvenue ! Veuillez choisir la langue de l'interface :",
        "de": "🌍 Willkommen! Bitte wählen Sie die Sprache der Benutzeroberfläche:",
        "es": "🌍 ¡Bienvenido! Por favor elige el idioma de la interfaz:",
        "ru": "🌍 Добро пожаловать! Пожалуйста, выберите язык интерфейса:",
        "zh": "🌍 欢迎！请选择界面语言：",
        "ja": "🌍 ようこそ！インターフェース言語を選択してください：",
    },
    "welcome_instructions": {
        "ar": (
            "👋 أهلاً بك في اختبار تحديد مستوى اللغة العربية!\n\n"
            "📌 سيتكون الاختبار من 9 أسئلة تشمل: المفردات، القواعد، القراءة، والاستماع.\n"
            "📌 اختر إجابة واحدة فقط لكل سؤال بالضغط على الزر.\n"
            "📌 في نهاية الاختبار ستحصل على نتيجتك ومستواك اللغوي فوراً.\n\n"
            "اضغط الزر أدناه لبدء الاختبار."
        ),
        "tr": (
            "👋 Arapça Seviye Tespit Sınavına hoş geldiniz!\n\n"
            "📌 Sınav; kelime bilgisi, dil bilgisi, okuma ve dinleme dahil 9 sorudan oluşur.\n"
            "📌 Her soru için butona tıklayarak sadece bir cevap seçin.\n"
            "📌 Sınav sonunda anında sonucunuzu ve seviyenizi öğreneceksiniz.\n\n"
            "Sınavı başlatmak için aşağıdaki butona tıklayın."
        ),
        "en": (
            "👋 Welcome to the Arabic Level Placement Test!\n\n"
            "📌 The test consists of 9 questions covering: vocabulary, grammar, reading, and listening.\n"
            "📌 Choose only one answer per question by tapping the button.\n"
            "📌 At the end of the test, you will instantly get your score and level.\n\n"
            "Tap the button below to start the test."
        ),
        "fr": (
            "👋 Bienvenue au test de niveau d'arabe !\n\n"
            "📌 Le test comporte 9 questions couvrant : vocabulaire, grammaire, lecture et écoute.\n"
            "📌 Choisissez une seule réponse par question en appuyant sur le bouton.\n"
            "📌 À la fin du test, vous obtiendrez immédiatement votre score et votre niveau.\n\n"
            "Appuyez sur le bouton ci-dessous pour commencer."
        ),
        "de": (
            "👋 Willkommen zum Arabisch-Einstufungstest!\n\n"
            "📌 Der Test besteht aus 9 Fragen zu: Wortschatz, Grammatik, Lesen und Hören.\n"
            "📌 Wählen Sie pro Frage nur eine Antwort durch Tippen auf die Schaltfläche.\n"
            "📌 Am Ende erhalten Sie sofort Ihr Ergebnis und Ihr Niveau.\n\n"
            "Tippen Sie unten, um den Test zu starten."
        ),
        "es": (
            "👋 ¡Bienvenido a la prueba de nivel de árabe!\n\n"
            "📌 La prueba consta de 9 preguntas sobre: vocabulario, gramática, lectura y comprensión auditiva.\n"
            "📌 Elige solo una respuesta por pregunta pulsando el botón.\n"
            "📌 Al final obtendrás tu puntuación y nivel de inmediato.\n\n"
            "Pulsa el botón de abajo para comenzar."
        ),
        "ru": (
            "👋 Добро пожаловать на тест по определению уровня арабского языка!\n\n"
            "📌 Тест состоит из 9 вопросов: лексика, грамматика, чтение и аудирование.\n"
            "📌 Выберите один ответ на каждый вопрос, нажав кнопку.\n"
            "📌 В конце теста вы сразу узнаете свой результат и уровень.\n\n"
            "Нажмите кнопку ниже, чтобы начать тест."
        ),
        "zh": (
            "👋 欢迎参加阿拉伯语水平测试！\n\n"
            "📌 测试共9道题，包括：词汇、语法、阅读和听力。\n"
            "📌 每题请点击按钮选择一个答案。\n"
            "📌 测试结束后将立即显示您的分数和等级。\n\n"
            "点击下方按钮开始测试。"
        ),
        "ja": (
            "👋 アラビア語レベル判定テストへようこそ！\n\n"
            "📌 このテストは語彙・文法・読解・リスニングを含む9問で構成されています。\n"
            "📌 各問題でボタンをタップして1つだけ回答を選んでください。\n"
            "📌 テスト終了後、すぐに結果とレベルが表示されます。\n\n"
            "下のボタンをタップしてテストを開始してください。"
        ),
    },
    "start_test_button": {
        "ar": "🚀 بدء الاختبار",
        "tr": "🚀 Testi Başlat",
        "en": "🚀 Start Test",
        "fr": "🚀 Commencer le test",
        "de": "🚀 Test starten",
        "es": "🚀 Comenzar la prueba",
        "ru": "🚀 Начать тест",
        "zh": "🚀 开始测试",
        "ja": "🚀 テストを開始",
    },
    "listening_intro": {
        "ar": "🎧 السؤال الأخير: مهارة الاستماع\n\nاستمع جيداً إلى الملف الصوتي التالي، ثم اضغط على الزر أدناه للإجابة على السؤال.",
        "tr": "🎧 Son soru: Dinleme becerisi\n\nAşağıdaki ses dosyasını dikkatlice dinleyin, ardından soruyu cevaplamak için aşağıdaki butona tıklayın.",
        "en": "🎧 Last question: Listening skill\n\nListen carefully to the following audio file, then tap the button below to answer the question.",
        "fr": "🎧 Dernière question : compréhension orale\n\nÉcoutez attentivement le fichier audio suivant, puis appuyez sur le bouton ci-dessous pour répondre.",
        "de": "🎧 Letzte Frage: Hörverständnis\n\nHören Sie sich die folgende Audiodatei aufmerksam an und tippen Sie dann unten, um die Frage zu beantworten.",
        "es": "🎧 Última pregunta: comprensión auditiva\n\nEscucha atentamente el siguiente archivo de audio y luego pulsa el botón de abajo para responder.",
        "ru": "🎧 Последний вопрос: аудирование\n\nВнимательно прослушайте следующий аудиофайл, затем нажмите кнопку ниже, чтобы ответить на вопрос.",
        "zh": "🎧 最后一题：听力\n\n请仔细听以下音频文件，然后点击下方按钮回答问题。",
        "ja": "🎧 最後の質問：リスニング\n\n次の音声ファイルをよく聞いてから、下のボタンをタップして質問に答えてください。",
    },
    "answer_question_button": {
        "ar": "✅ الإجابة على السؤال",
        "tr": "✅ Soruyu Cevapla",
        "en": "✅ Answer Question",
        "fr": "✅ Répondre à la question",
        "de": "✅ Frage beantworten",
        "es": "✅ Responder pregunta",
        "ru": "✅ Ответить на вопрос",
        "zh": "✅ 回答问题",
        "ja": "✅ 質問に答える",
    },
    "reading_passage_title": {
        "ar": "📖 اقرأ النص الآتي، ثم اختر الإجابة الصحيحة:",
        "tr": "📖 Aşağıdaki metni okuyun, ardından doğru cevabı seçin:",
        "en": "📖 Read the following passage, then choose the correct answer:",
        "fr": "📖 Lisez le texte suivant, puis choisissez la bonne réponse :",
        "de": "📖 Lesen Sie den folgenden Text und wählen Sie dann die richtige Antwort:",
        "es": "📖 Lee el siguiente texto y elige la respuesta correcta:",
        "ru": "📖 Прочитайте следующий текст, затем выберите правильный ответ:",
        "zh": "📖 阅读以下短文，然后选择正确答案：",
        "ja": "📖 次の文章を読んで、正しい答えを選んでください：",
    },
    "question_progress": {
        "ar": "السؤال {current} من {total}",
        "tr": "Soru {current} / {total}",
        "en": "Question {current} of {total}",
        "fr": "Question {current} sur {total}",
        "de": "Frage {current} von {total}",
        "es": "Pregunta {current} de {total}",
        "ru": "Вопрос {current} из {total}",
        "zh": "第 {current} / {total} 题",
        "ja": "質問 {current} / {total}",
    },
    "result_title": {
        "ar": "🎉 نتيجة الاختبار",
        "tr": "🎉 Sınav Sonucu",
        "en": "🎉 Test Result",
        "fr": "🎉 Résultat du test",
        "de": "🎉 Testergebnis",
        "es": "🎉 Resultado de la prueba",
        "ru": "🎉 Результат теста",
        "zh": "🎉 测试结果",
        "ja": "🎉 テスト結果",
    },
    "result_score": {
        "ar": "📊 درجتك الكلية: {score} من 100\n✅ عدد الإجابات الصحيحة: {correct} من {total}",
        "tr": "📊 Toplam puanınız: {score} / 100\n✅ Doğru cevap sayısı: {correct} / {total}",
        "en": "📊 Your total score: {score} out of 100\n✅ Correct answers: {correct} out of {total}",
        "fr": "📊 Votre score total : {score} sur 100\n✅ Réponses correctes : {correct} sur {total}",
        "de": "📊 Ihre Gesamtpunktzahl: {score} von 100\n✅ Richtige Antworten: {correct} von {total}",
        "es": "📊 Tu puntuación total: {score} de 100\n✅ Respuestas correctas: {correct} de {total}",
        "ru": "📊 Ваш общий балл: {score} из 100\n✅ Правильных ответов: {correct} из {total}",
        "zh": "📊 您的总分：{score} / 100\n✅ 正确答案数：{correct} / {total}",
        "ja": "📊 総合スコア：{score} / 100\n✅ 正解数：{correct} / {total}",
    },
    "result_level": {
        "ar": "🏆 مستواك اللغوي: {level}",
        "tr": "🏆 Dil seviyeniz: {level}",
        "en": "🏆 Your language level: {level}",
        "fr": "🏆 Votre niveau de langue : {level}",
        "de": "🏆 Ihr Sprachniveau: {level}",
        "es": "🏆 Tu nivel de idioma: {level}",
        "ru": "🏆 Ваш языковой уровень: {level}",
        "zh": "🏆 您的语言等级：{level}",
        "ja": "🏆 あなたの言語レベル：{level}",
    },
    "restart_hint": {
        "ar": "🔄 يمكنك إعادة الاختبار في أي وقت عبر إرسال الأمر /start",
        "tr": "🔄 /start komutunu göndererek testi istediğiniz zaman tekrar başlatabilirsiniz.",
        "en": "🔄 You can retake the test anytime by sending the /start command.",
        "fr": "🔄 Vous pouvez repasser le test à tout moment en envoyant la commande /start.",
        "de": "🔄 Sie können den Test jederzeit erneut starten, indem Sie /start senden.",
        "es": "🔄 Puedes volver a hacer la prueba en cualquier momento enviando el comando /start.",
        "ru": "🔄 Вы можете пройти тест повторно в любое время, отправив команду /start.",
        "zh": "🔄 您可以随时发送 /start 命令重新参加测试。",
        "ja": "🔄 /start コマンドを送信すればいつでもテストを再受験できます。",
    },
    "audio_send_error": {
        "ar": "⚠️ تعذّر إرسال الملف الصوتي تلقائياً. يمكنك الاستماع إليه عبر هذا الرابط:\n{link}",
        "tr": "⚠️ Ses dosyası otomatik olarak gönderilemedi. Bu bağlantı üzerinden dinleyebilirsiniz:\n{link}",
        "en": "⚠️ Could not send the audio file automatically. You can listen to it via this link:\n{link}",
        "fr": "⚠️ Impossible d'envoyer le fichier audio automatiquement. Vous pouvez l'écouter via ce lien :\n{link}",
        "de": "⚠️ Die Audiodatei konnte nicht automatisch gesendet werden. Sie können sie über diesen Link anhören:\n{link}",
        "es": "⚠️ No se pudo enviar el archivo de audio automáticamente. Puedes escucharlo en este enlace:\n{link}",
        "ru": "⚠️ Не удалось автоматически отправить аудиофайл. Вы можете прослушать его по этой ссылке:\n{link}",
        "zh": "⚠️ 无法自动发送音频文件。您可以通过此链接收听：\n{link}",
        "ja": "⚠️ 音声ファイルを自動送信できませんでした。こちらのリンクからお聞きいただけます：\n{link}",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """يجلب النص المترجم حسب المفتاح واللغة، مع دعم fallback للإنجليزية."""
    entry = TEXTS.get(key, {})
    text = entry.get(lang) or entry.get("en") or ""
    if kwargs:
        text = text.format(**kwargs)
    return text
