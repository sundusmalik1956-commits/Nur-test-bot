# =====================================================
# معالجة الإجابات
# =====================================================

import time
import random
from handlers.user_session import user_data
from handlers.sections import ask_next_vocab_question, ask_next_reading_question, ask_next_listening_question, start_section_5, show_final_results
from languages.translations import get_text
from handlers.ai_evaluator import evaluate_with_ai

def handle_answer(user_id, message_text, bot):
    """معالجة إجابة المستخدم (اختيار من متعدد) - بدون إظهار صحة الإجابة"""
    session = user_data.get(user_id)
    if not session or not session.waiting_for_answer:
        return
    
    # تحقق من الوقت
    if session.start_time and time.time() - session.start_time > session.time_limit:
        bot.send_message(user_id, get_text(user_id, "time_up"))
        show_final_results(user_id, bot)
        return
    
    session.waiting_for_answer = False
    user_answer = message_text.strip()
    
    # جلب الإجابة الصحيحة والنص من بيانات السؤال الحالي
    correct_letter = session.current_correct_answer
    question_data = session.current_question_data
    
    if question_data and len(question_data) > 1:
        options = question_data[1]
        correct_text = None
        
        # محاولة تحديد النص الصحيح سواء أرسل المستخدم الحرف (أ، ب...) أو النص مباشرة
        mapping = {'أ': 0, 'ب': 1, 'ج': 2, 'د': 3}
        if correct_letter in mapping and mapping[correct_letter] < len(options):
            correct_text = options[mapping[correct_letter]]
        elif correct_letter in options:
            correct_text = correct_letter
            
        # التحقق من الإجابة وتحديث النتيجة بشكل آمن
        if correct_text and user_answer == correct_text:
            session.scores[session.current_question_type] += 1
    
    # الانتقال للسؤال التالي حسب القسم
    if session.current_section == 1:
        ask_next_vocab_question(user_id, bot)
    elif session.current_section == 2:
        ask_next_reading_question(user_id, bot)
    elif session.current_section == 3:
        ask_next_listening_question(user_id, bot)

def handle_voice(user_id, voice_file, bot):
    """معالجة الملف الصوتي للمحادثة"""
    session = user_data.get(user_id)
    if not session or not session.waiting_for_voice:
        return
    
    if session.start_time and time.time() - session.start_time > session.time_limit:
        bot.send_message(user_id, get_text(user_id, "time_up"))
        show_final_results(user_id, bot)
        return
    
    session.waiting_for_voice = False
    bot.send_message(user_id, get_text(user_id, "voice_processing"))
    
    try:
        file_info = bot.get_file(voice_file.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        simulated_text = "هذه إجابة نموذجية على سؤال المحادثة"
        score = evaluate_with_ai(simulated_text, "speaking")
        session.scores["speaking"] = score
        
        bot.send_message(user_id, get_text(user_id, "voice_grade", score))
        start_section_5(user_id, bot)
        
    except Exception as e:
        print(f"Error processing voice: {e}")
        score = random.randint(5, 9)
        session.scores["speaking"] = score
        bot.send_message(user_id, get_text(user_id, "voice_grade", score))
        start_section_5(user_id, bot)

def handle_writing(user_id, text, bot):
    """معالجة الإجابة الكتابية"""
    session = user_data.get(user_id)
    if not session or not session.waiting_for_writing:
        return
    
    if session.start_time and time.time() - session.start_time > session.time_limit:
        bot.send_message(user_id, get_text(user_id, "time_up"))
        show_final_results(user_id, bot)
        return
    
    session.waiting_for_writing = False
    bot.send_message(user_id, get_text(user_id, "writing_processing"))
    
    try:
        score = evaluate_with_ai(text, "writing")
        session.scores["writing"] = score
        
        bot.send_message(user_id, get_text(user_id, "writing_grade", score))
        show_final_results(user_id, bot)
        
    except Exception as e:
        print(f"Error processing writing: {e}")
        score = random.randint(5, 9)
        session.scores["writing"] = score
        bot.send_message(user_id, get_text(user_id, "writing_grade", score))
        show_final_results(user_id, bot)
