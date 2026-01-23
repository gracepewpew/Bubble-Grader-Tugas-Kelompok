import os
from .models import StudentResult, AnswerKey

# Cuma import Interface/Class typing aja buat Type Hinting (DIP Friendly)
from .utils.ui import UserInterface
from .utils.file_manager import FileManager
from .reporting.report_manager import ReportManager
from .grading.grader import Grader

class ExamGraderApp:
    #  FACADE PATTERN 
    # Class ini bertindak sebagai "Facade" (Wajah Depan).
    # User atau Main program gak perlu tau ribetnya ngurus FileManager atau Grader.
    # Cukup panggil app.run(), class ini yang ngatur lalu lintasnya.

    #  DIP (Dependency Inversion Principle) 
    # Perhatiin deh, kita gak ada 'new UserInterface()' di sini.
    # Semua tools dikasih lewat parameter (Constructor Injection).
    # Ini bikin App gampang dites dan fleksibel.
    def __init__(
        self, 
        ui: UserInterface, 
        file_manager: FileManager, 
        grader: Grader, 
        report_manager: ReportManager
    ):
        self.ui = ui
        self.file_manager = file_manager
        self.grader = grader
        self.report_manager = report_manager
    
    def _start_grading_session(self):
        # Minta UI buat nanya user mau nilai mapel apa
        student_answers_path, answer_key_path = self.ui.get_grading_paths(self.file_manager)
        
        if not student_answers_path or not answer_key_path: 
            return

        # Factory Method dipanggil di sini (AnswerKey.from_file)
        answer_key = AnswerKey.from_file(answer_key_path)
        if not answer_key:
            self.ui.display_progress("Gagal memuat kunci jawaban. Kembali ke menu utama.")
            return

        # Pake generator biar hemat memori kalau datanya ribuan
        student_answer_files = self.file_manager.find_student_answer_files(student_answers_path)
        
        # Convert ke list dulu buat ngecek kosong/enggak (karena generator cuma bisa sekali baca)
        files_list = list(student_answer_files)
        if not files_list:
             self.ui.display_progress("Tidak ada file jawaban siswa ditemukan.")
             return

        all_results = []
        class_name_for_report = ""

        # Loop processing utama
        for i, file_path in enumerate(files_list):
            sheet_data = self.file_manager.load_json_data(file_path)
            if not sheet_data:
                continue

            student_info = sheet_data.get("student_info", {})
            student_name = student_info.get("name", "Unknown")
            class_name = student_info.get("class", "Unknown")
            
            if not class_name_for_report:
                class_name_for_report = class_name
            
            # Grader bekerja di sini! Dia bakal otomatis milih strategi penilaian
            score = self.grader.grade_sheet(sheet_data, answer_key)
            
            result = StudentResult(number=i+1, name=student_name, class_name=class_name, score=round(score, 2))
            all_results.append(result)

        if not os.path.exists('output'):
            os.makedirs('output')

        report_filename = f"{answer_key.subject.replace(' ', '_')}_{class_name_for_report.replace(' ', '_')}" if class_name_for_report else "Unknown_Class_Report"
        
        # Delegasi ke ReportManager (SRP: App gak urus cara bikin Excel, cuma nyuruh doang)
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
                self.ui.display_progress("\nPilihan tidak valid.")