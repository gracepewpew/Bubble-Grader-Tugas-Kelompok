import os
import json

class FileManager:
    BASE_DIR = "input_data"
    KEYS_DIR = "answer_keys"
    ANSWERS_DIR = "student_answers"

    def get_available_subjects(self) -> list[str]:
        path = os.path.join(self.BASE_DIR, self.KEYS_DIR)
        if not os.path.exists(path):
            return []
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    def get_keys_for_subject(self, subject: str) -> list[str]:
        path = os.path.join(self.BASE_DIR, self.KEYS_DIR, subject)
        if not os.path.exists(path):
            return []
        return [f for f in os.listdir(path) if f.endswith('.json')]

    def get_full_key_path(self, subject: str, filename: str) -> str:
        return os.path.join(self.BASE_DIR, self.KEYS_DIR, subject, filename)

    def find_student_answer_files(self, directory_path: str = None):
        if directory_path is None:
            directory_path = os.path.join(self.BASE_DIR, self.ANSWERS_DIR)
            
        if not os.path.isdir(directory_path):
            return

        for root, dirs, files in os.walk(directory_path):
            for f in files:
                if f.endswith('.json'):
                    yield os.path.join(root, f)
    
    def load_json_data(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}