import os
from .utils.ui import UserInterface
from .utils.file_manager import FileManager
from .models import StudentResult, AnswerKey
from .grading.grader import DebugGrader
from .grading.grading_types import MCQGradingType, ShortAnswerGradingType, EssayGradingType
from .reporting.report_manager import ReportManager

class ExamGraderApp:
    def __init__(self):
        self.ui = UserInterface()
        self.file_manager = FileManager()
        self.report_manager = ReportManager()
        grading_types = {
            "mcq": MCQGradingType(),
            "short_answer": ShortAnswerGradingType(),
            "essay": EssayGradingType(self.ui)
        }
        self.grader = DebugGrader(grading_types)
    
    def _start_grading_session(self):
        student_answers_path, answer_key_path = self.ui.get_grading_paths()
        
        answer_key = AnswerKey.from_file(answer_key_path)
        if not answer_key:
            self.ui.display_progress("Gagal memuat kunci jawaban. Kembali ke menu utama.")
            return

        student_answer_files = self.file_manager.find_student_answer_files(student_answers_path)
        if not student_answer_files:
            self.ui.display_progress(f"Tidak ada file jawaban siswa (.json) ditemukan di '{student_answers_path}'. Kembali ke menu utama.")
            return

        all_results = []
        class_name_for_report = ""
        for i, file_path in enumerate(student_answer_files):
            sheet_data = self.file_manager.load_json_data(file_path)
            if not sheet_data:
                self.ui.display_progress(f"Melewatkan file rusak: {file_path}")
                continue

            student_info = sheet_data.get("student_info", {})
            student_name = student_info.get("name", "Unknown")
            class_name = student_info.get("class", "Unknown")
            
            if not class_name_for_report:
                class_name_for_report = class_name
            
            score = self.grader.grade_sheet(sheet_data, answer_key)
            result = StudentResult(number=i+1, name=student_name, class_name=class_name, score=round(score, 2))
            all_results.append(result)

        if not os.path.exists('output'):
            os.makedirs('output')

        report_filename = f"{answer_key.subject.replace(' ', '_')}_{class_name_for_report.replace(' ', '_')}"
        self.report_manager.generate_all_reports(all_results, report_filename)
        
        self.ui.display_progress("\nSesi penilaian selesai!")
        input("Tekan Enter untuk kembali ke menu utama...")

    def run(self):
        while True:
            choice = self.ui.display_main_menu()
            
            if choice == '1':
                self.ui.display_how_to_use()
            elif choice == '2':
                self._start_grading_session()
            elif choice == '3':
                self.ui.display_exit_message()
                break
            else:
                self.ui.display_progress("\nPilihan tidak valid. Silakan coba lagi.")