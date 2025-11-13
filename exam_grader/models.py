from dataclasses import dataclass, asdict
import json

@dataclass
class StudentResult:
    number: int
    name: str
    class_name: str
    score: float

    def to_dict(self):
        return asdict(self)

class AnswerKey:
    def __init__(self, key_data: dict):
        self.subject = key_data.get("subject", "Unknown Subject")
        self.class_name = key_data.get("class_name", "Unknown Class")
        self.sections = key_data.get("sections", {})

    @classmethod
    def from_file(cls, file_path: str):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return cls(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def get_section_key(self, section_id: str) -> dict:
        return self.sections.get(section_id, {}).get("answers", {})