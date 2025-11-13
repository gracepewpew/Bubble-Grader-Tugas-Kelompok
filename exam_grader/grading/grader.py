from .grading_types import IGradingType
from ..models import AnswerKey

class Grader:
    def __init__(self, grading_types: dict[str, IGradingType]):
        self._grading_types = grading_types

    def grade_sheet(self, sheet_data: dict, answer_key: AnswerKey) -> float:
        total_points_awarded = 0.0
        total_possible_points = 0.0

        student_info = sheet_data.get("student_info", {}) 
        student_answers_all_sections = sheet_data.get("answers", {})

        for section_id, section_key_data in answer_key.sections.items():
            section_type = section_key_data.get("type")
            grader_for_section = self._grading_types.get(section_type)

            if grader_for_section:
                student_answers_for_section = student_answers_all_sections.get(section_id, {})
                
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

class DebugGrader(Grader):
    def grade_sheet(self, sheet_data: dict, answer_key: AnswerKey) -> float:
        print("\n" + "="*70)
        print(f"--- DEBUG MODE: Analyzing Sheet for {sheet_data.get('student_info', {}).get('name', 'N/A')} ---")
        
        final_score = super().grade_sheet(sheet_data, answer_key)
        
        print("\n" + "-"*70)
        print(f"Final Calculated Score (from logic): {final_score:.2f}%")
        print("="*70)
        
        return final_score