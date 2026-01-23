from .grading_types import IGradingType
from ..models import AnswerKey

class Grader:
    def __init__(self, grading_types: dict[str, IGradingType]):
        # Simpan daftar strategi yang tersedia (mcq, essay, dll)
        self._grading_types = grading_types

    def grade_sheet(self, sheet_data: dict, answer_key: AnswerKey) -> float:
        total_points_awarded = 0.0
        total_possible_points = 0.0

        student_info = sheet_data.get("student_info", {}) 
        student_answers_all_sections = sheet_data.get("answers", {})

        # Loop setiap section soal (Bagian A, Bagian B, dst)
        for section_id, section_key_data in answer_key.sections.items():
            section_type = section_key_data.get("type")
            
            # --- STRATEGY PATTERN IN ACTION ---
            # Di sini magic-nya. Kita ambil strategi penilai yang cocok (misal: "mcq").
            grader_for_section = self._grading_types.get(section_type)

            if grader_for_section:
                student_answers_for_section = student_answers_all_sections.get(section_id, {})
                
                # Delegasikan penilaian ke strategi tersebut
                awarded, possible = grader_for_section.grade(
                    student_info, 
                    student_answers_for_section, 
                    section_key_data["answers"]
                )
                total_points_awarded += awarded
                total_possible_points += possible

        if total_possible_points == 0:
            return 0.0

        return (total_points_awarded / total_possible_points) * 100

# --- LSP (Liskov Substitution Principle) & OCP ---
# DebugGrader adalah turunan Grader. Dia nambahin fitur "print debug",
# TAPI dia gak ngubah cara kerja utamanya.
# Kita bisa ganti 'Grader' biasa dengan 'DebugGrader' di main.py tanpa bikin program crash.
# Ini bukti class ini Open for Extension (bisa di-extend jadi debug), Closed for Modification.
class DebugGrader(Grader):
    def grade_sheet(self, sheet_data: dict, answer_key: AnswerKey) -> float:
        print("\n" + "="*70)
        print(f"--- DEBUG MODE: Analyzing Sheet for {sheet_data.get('student_info', {}).get('name', 'N/A')} ---")
        
        # Panggil method orang tua (super) buat hitung nilai aslinya
        final_score = super().grade_sheet(sheet_data, answer_key)
        
        print("\n" + "-"*70)
        print(f"Final Calculated Score (from logic): {final_score:.2f}%")
        print("="*70)
        
        return final_score