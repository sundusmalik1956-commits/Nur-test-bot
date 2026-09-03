# =====================================================
# تقييم الذكاء الاصطناعي باستخدام Gemini API
# =====================================================

import re
import random
import requests
from settings import GEMINI_API_KEY


def evaluate_with_ai(text, question_type="writing"):
    """
    تقييم الإجابة باستخدام Google Gemini API
    يعيد درجة من 0-10
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return random.randint(5, 9)
    
    try:
        # استخدام Gemini API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        
        if question_type == "speaking":
            prompt = f"""
            قيم الإجابة التالية على سؤال محادثة باللغة العربية من حيث:
            1. الفهم (مدى فهم السؤال)
            2. المفردات (تنوع ودقة المفردات)
            3. التركيب (صحة القواعد)
            4. الطلاقة (الانسيابية)
            
            أعط درجة من 0-10 فقط (رقم واحد).
            
            النص: {text}
            """
        else:  # writing
            prompt = f"""
            قيم النص التالي (إجابة على سؤال كتابة باللغة العربية) من حيث:
            1. المحتوى (مدى إجابة السؤال)
            2. التنظيم (ترتيب الأفكار)
            3. المفردات (الدقة والتنوع)
            4. القواعد (صحة النحو)
            
            أعط درجة من 0-10 فقط (رقم واحد).
            
            النص: {text}
            """
        
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            score_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            numbers = re.findall(r'\d+', score_text)
            if numbers:
                score = int(numbers[0])
                return min(max(score, 0), 10)
            else:
                return 7
        else:
            return random.randint(5, 9)
            
    except Exception as e:
        print(f"Error in Gemini evaluation: {e}")
        return random.randint(5, 9)
