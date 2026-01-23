from abc import ABC, abstractmethod

# --- ISP (Interface Segregation Principle) ---
# Ini kontrak kecil khusus buat nanya nilai Essay.
# Kenapa dipisah? Biar EssayGradingType gak perlu tau seluruh isi "UserInterface" yang kegedean.
# Dia cuma butuh tau: "Ada method get_essay_score yang balikin float".
# Jadi kalau nanti ganti UI ke Web/Bot, kontrak ini tetap aman dan ringan.
class IScoreInputProvider(ABC):
    @abstractmethod
    def get_essay_score(self, student_name: str, student_answer: str, question_prompt: str, max_points: int) -> float:
        pass

# --- STRATEGY PATTERN (Interface) ---
# Ini blueprint utama buat semua strategi penilaian.
# Penerapan OCP (Open/Closed Principle) ada di sini.
# Kalau mau nambah tipe soal baru (misal: Mencocokkan), tinggal bikin class baru
# yang implement method grade() ini. Gak perlu ngacak-ngacak kode yang udah ada.
class IGradingType(ABC):
    @abstractmethod
    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        pass

# --- Concrete Strategy 1: MCQ ---
# SRP (Single Responsibility Principle): Class ini CUMA mikirin logic nilai Pilihan Ganda.
class MCQGradingType(IGradingType):
    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        points_awarded = 0.0
        possible_points = 0.0

        for q_num, key_info in section_key.items():
            correct_answer = key_info["answer"]
            points = key_info["points"]
            possible_points += points

            student_answer = student_answers.get(q_num)
            if student_answer == correct_answer:
                points_awarded += points
        
        return points_awarded, possible_points

# --- Concrete Strategy 2: Short Answer ---
# SRP: Class ini CUMA mikirin logic nilai Isian Singkat (pake logika lower() biar gak case-sensitive).
class ShortAnswerGradingType(IGradingType):
    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        points_awarded = 0.0
        possible_points = 0.0

        for q_num, key_info in section_key.items():
            correct_answer = key_info["answer"].lower()
            points = key_info["points"]
            possible_points += points
            
            # Logic unik di sini: kita lower() input siswa biar 'Apel' sama dengan 'apel'
            student_answer = student_answers.get(q_num, "").lower()

            if student_answer == correct_answer:
                points_awarded += points
        
        return points_awarded, possible_points

# --- Concrete Strategy 3: Essay ---
# Bagian ini agak spesial karena butuh interaksi manusia.
class EssayGradingType(IGradingType):
    
    # --- DIP (Dependency Inversion Principle) ---
    # Perhatiin deh, kita inject 'input_provider' di sini.
    # Kita bergantung sama ABSTRAKSI (IScoreInputProvider), bukan KONKRET (UserInterface).
    # Jadi module Grading bener-bener terpisah dari module UI. Loose Coupling banget!
    def __init__(self, input_provider: IScoreInputProvider):
        self._input_provider = input_provider

    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        points_awarded = 0.0
        possible_points = 0.0
        student_name = student_info.get("name", "Unknown Student")

        for q_num, key_info in section_key.items():
            question_prompt = key_info["prompt"]
            points = key_info["points"]
            possible_points += points
            
            student_answer = student_answers.get(q_num, "(jawaban kosong)")

            # Minta nilai lewat provider (interface).
            # Si Grader gak peduli nilainya diketik di console atau dikirim lewat internet,
            # yang penting dapet angka balikannya.
            awarded = self._input_provider.get_essay_score(student_name, student_answer, question_prompt, points)
            points_awarded += awarded
            
        return points_awarded, possible_points