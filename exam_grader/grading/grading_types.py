from abc import ABC, abstractmethod
from ..utils.ui import UserInterface

class IGradingType(ABC):
    @abstractmethod
    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        pass

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

class ShortAnswerGradingType(IGradingType):
    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        points_awarded = 0.0
        possible_points = 0.0

        for q_num, key_info in section_key.items():
            correct_answer = key_info["answer"].lower()
            points = key_info["points"]
            possible_points += points
            
            student_answer = student_answers.get(q_num, "").lower()

            if student_answer == correct_answer:
                points_awarded += points
        
        return points_awarded, possible_points

class EssayGradingType(IGradingType):
    def __init__(self, ui: UserInterface):
        self._ui = ui

    def grade(self, student_info: dict, student_answers: dict, section_key: dict) -> tuple[float, float]:
        points_awarded = 0.0
        possible_points = 0.0
        student_name = student_info.get("name", "Unknown Student")

        for q_num, key_info in section_key.items():
            question_prompt = key_info["prompt"]
            points = key_info["points"]
            possible_points += points
            
            student_answer = student_answers.get(q_num, "(jawaban kosong)")

            awarded = self._ui.prompt_for_essay_score(student_name, student_answer, question_prompt, points)
            points_awarded += awarded
            
        return points_awarded, possible_points