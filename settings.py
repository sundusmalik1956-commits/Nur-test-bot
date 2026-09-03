import os

# =====================================================
# متغيرات البيئة
# =====================================================

TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# =====================================================
# إعدادات الاختبار
# =====================================================

TEST_DURATION = 30 * 60  # 30 دقيقة
QUESTIONS_PER_SECTION = 10
MAX_VOICE_DURATION = 60  # 60 ثانية كحد أقصى للتسجيل الصوتي
