# =====================================================
# هيكل بيانات المستخدمين
# =====================================================

user_data = {}

class UserSession:
    def __init__(self, user_id, language="arabic"):
        self.user_id = user_id
        self.language = language
        self.start_time = None
        self.time_limit = 30 * 60  # 30 دقيقة
        self.current_section = 0
        self.scores = {"vocab": 0, "reading": 0, "listening": 0, "speaking": 0, "writing": 0}
        self.vocab_questions = []
        self.vocab_index = 0
        self.reading_index = 0
        self.reading_text_index = 0
        self.listening_index = 0
        self.listening_text_index = 0
        self.current_speaking_question = None
        self.current_writing_question = None
        self.is_finished = False
        self.waiting_for_voice = False
        self.waiting_for_writing = False
        self.waiting_for_answer = False
        self.current_correct_answer = None
        self.current_question_type = None
        self.current_question_data = None
        self.answered_vocab = 0
        self.answered_reading = 0
        self.answered_listening = 0
