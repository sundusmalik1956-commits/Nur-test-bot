# =====================================================
# دوال الأقسام المختلفة
# =====================================================

import random
import time
from handlers.user_session import user_data
from languages.translations import get_text
from data.questions_vocab import QUESTIONS_VOCAB_GRAMMAR
from data.questions_reading import READING_TEXTS
from data.questions_listening import LISTENING_TEXTS
from data.questions_speaking import CONVERSATION_QUESTIONS
from data.questions_writing import WRITING_QUESTIONS

def shuffle_vocab_questions():
    return random.sample(QUESTIONS_VOCAB_GRAMMAR, 10)

def start_section_1(user_id, bot):
    session = user_data.get(user_id)
    if not session: return
    
    session.current_section = 1
    session.vocab_questions = shuffle_vocab_questions()
    session.vocab_index = 0
    session.answered_vocab = 0
    session.scores["vocab"] = 0
    
    bot.send_message(user_id, get_text(user_id, "section_1"))
    time.sleep(1)
    ask_next_vocab_question(user_id, bot)

def ask_next_vocab_question(user_id, bot):
    session = user_data.get(user_id)
    if not session or session.answered_vocab >= 10:
        bot.send_message(user_id, f"{get_text(user_id, 'section_1')} - {get_text(user_id, 'finish')}")
        start_section_2(user_id, bot)
        return
    
    question, options, correct = session.vocab_questions[session.vocab_index]
    
    from keyboards.buttons import create_options_keyboard
    markup = create_options_keyboard(options)
    
    bot.send_message(
        user_id, 
        f"📝 السؤال {session.answered_vocab + 1}/10\n\n{question}", 
        reply_markup=markup
    )
    session.waiting_for_answer = True
    session.current_correct_answer = correct
    session.current_question_type = "vocab"
    session.current_question_data = (question, options, correct)
    session.vocab_index += 1
    session.answered_vocab += 1

def start_section_2(user_id, bot):
    session = user_data.get(user_id)
    if not session: return
    
    session.current_section = 2
    session.reading_index = 0
    session.reading_text_index = random.randint(0, len(READING_TEXTS) - 1)
    session.answered_reading = 0
    session.scores["reading"] = 0
    
    bot.send_message(user_id, get_text(user_id, "section_2"))
    text_data = READING_TEXTS[session.reading_text_index]
    bot.send_message(user_id, text_data["text"])
    time.sleep(2)
    ask_next_reading_question(user_id, bot)

def ask_next_reading_question(user_id, bot):
    session = user_data.get(user_id)
    if not session or session.answered_reading >= 10:
        bot.send_message(user_id, f"{get_text(user_id, 'section_2')} - {get_text(user_id, 'finish')}")
        start_section_3(user_id, bot)
        return
    
    text_data = READING_TEXTS[session.reading_text_index]
    question, options, correct = text_data["questions"][session.reading_index]
    
    from keyboards.buttons import create_options_keyboard
    markup = create_options_keyboard(options)
    
    bot.send_message(
        user_id, 
        f"📝 السؤال {session.answered_reading + 1}/10\n\n{question}", 
        reply_markup=markup
    )
    session.waiting_for_answer = True
    session.current_correct_answer = correct
    session.current_question_type = "reading"
    session.current_question_data = (question, options, correct)
    session.reading_index += 1
    session.answered_reading += 1

def start_section_3(user_id, bot):
    session = user_data.get(user_id)
    if not session: return
    
    session.current_section = 3
    session.listening_index = 0
    session.listening_text_index = random.randint(0, len(LISTENING_TEXTS) - 1)
    session.answered_listening = 0
    session.scores["listening"] = 0
    
    bot.send_message(user_id, get_text(user_id, "section_3"))
    
    text_data = LISTENING_TEXTS[session.listening_text_index]
    bot.send_message(user_id, get_text(user_id, "listening_instruction"))
    
    # معالجة آمنة لخطأ file_id لمنع توقف البوت في حال وجود خطأ بمعرّف الملف الصوتي
    try:
        audio_id = text_data.get("id")
        if audio_id:
            bot.send_audio(user_id, audio_id)
        else:
            bot.send_message(user_id, "🎵 (عذراً، الملف الصوتي غير متاح، سننتقل للأسئلة مباشرة)")
    except Exception as e:
        print(f"⚠️ Warning: Failed to send audio file: {e}")
        bot.send_message(user_id, "🎵 (تعذر إرسال الملف الصوتي، سننتقل للأسئلة مباشرة)")
    
    time.sleep(3)
    ask_next_listening_question(user_id, bot)

def ask_next_listening_question(user_id, bot):
    session = user_data.get(user_id)
    if not session or session.answered_listening >= 10:
        bot.send_message(user_id, f"{get_text(user_id, 'section_3')} - {get_text(user_id, 'finish')}")
        start_section_4(user_id, bot)
        return
    
    text_data = LISTENING_TEXTS[session.listening_text_index]
    question, options, correct = text_data["questions"][session.listening_index]
    
    from keyboards.buttons import create_options_keyboard
    markup = create_options_keyboard(options)
    
    bot.send_message(
        user_id, 
        f"📝 السؤال {session.answered_listening + 1}/10\n\n{question}", 
        reply_markup=markup
    )
    session.waiting_for_answer = True
    session.current_correct_answer = correct
    session.current_question_type = "listening"
    session.current_question_data = (question, options, correct)
    session.listening_index += 1
    session.answered_listening += 1

def start_section_4(user_id, bot):
    session = user_data.get(user_id)
    if not session: return
    
    session.current_section = 4
    session.current_speaking_question = random.choice(CONVERSATION_QUESTIONS)
    
    bot.send_message(user_id, get_text(user_id, "section_4"))
    bot.send_message(
        user_id, 
        f"{get_text(user_id, 'conversation_question_pre')}\n\n🎙️ {session.current_speaking_question}"
    )
    bot.send_message(
        user_id, 
        get_text(user_id, "record_voice")
    )
    session.waiting_for_voice = True

def start_section_5(user_id, bot):
    session = user_data.get(user_id)
    if not session: return
    
    session.current_section = 5
    session.current_writing_question = random.choice(WRITING_QUESTIONS)
    
    bot.send_message(user_id, get_text(user_id, "section_5"))
    bot.send_message(
        user_id, 
        f"{get_text(user_id, 'writing_question_pre')}\n\n✍️ {session.current_writing_question}"
    )
    bot.send_message(
        user_id, 
        get_text(user_id, "submit_text")
    )
    session.waiting_for_writing = True

def show_final_results(user_id, bot):
    """عرض النتيجة النهائية للمستخدم"""
    session = user_data.get(user_id)
    if not session: return
    
    total = sum(session.scores.values())
    level = get_level(total)
    level_name = get_level_name(total, user_id)
    grade = get_grade_name(total, user_id)
    
    result_text = get_text(
        user_id, "results",
        session.scores["vocab"],
        session.scores["reading"],
        session.scores["listening"],
        session.scores["speaking"],
        session.scores["writing"],
        total,
        level_name
    )
    result_text += f"\n\n📌 {get_text(user_id, 'grade')} {grade}"
    
    bot.send_message(user_id, result_text)
    session.is_finished = True

def get_level(score):
    if score >= 45: return "C1"
    elif score >= 35: return "B2"
    elif score >= 25: return "B1"
    elif score >= 15: return "A2"
    else: return "A1"

def get_level_name(score, user_id):
    if score >= 45: return get_text(user_id, "level_c1")
    elif score >= 35: return get_text(user_id, "level_b2")
    elif score >= 25: return get_text(user_id, "level_b1")
    elif score >= 15: return get_text(user_id, "level_a2")
    else: return get_text(user_id, "level_a1")

def get_grade_name(score, user_id):
    if score >= 45: return get_text(user_id, "perfect")
    elif score >= 35: return get_text(user_id, "good")
    elif score >= 25: return get_text(user_id, "average")
    elif score >= 15: return get_text(user_id, "below_average")
    else: return get_text(user_id, "poor")
