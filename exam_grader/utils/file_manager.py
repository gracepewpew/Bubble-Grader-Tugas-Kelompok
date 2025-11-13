import os
import json

class FileManager:
    def find_student_answer_files(self, directory_path: str) -> list[str]:
        if not os.path.isdir(directory_path):
            return []
        
        return [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if f.endswith('.json')
        ]

    def load_json_data(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {file_path}. Check for syntax errors.")
            return {}