from exam_grader.app import ExamGraderApp
from exam_grader.utils.ui import UserInterface
from exam_grader.utils.file_manager import FileManager
from exam_grader.reporting.report_manager import ReportManager
from exam_grader.reporting.generators import ExcelReportGenerator, PdfReportGenerator
from exam_grader.grading.grader import DebugGrader
from exam_grader.grading.grading_types import MCQGradingType, ShortAnswerGradingType, EssayGradingType

if __name__ == "__main__":
    #  SETUP DEPENDENCIES 
    # Di sini kita nerapin DIP (Dependency Inversion Principle).
    # Kita bikin dulu "tools"-nya di luar, baru nanti dikasih ke App.
    # Jadi si App gak perlu tau cara bikin tools-nya, tau make doang.
    
    ui = UserInterface()
    file_manager = FileManager()
    
    #  OCP (Open/Closed Principle) 
    # ReportManager didesain "Open for extension". 
    # Kalau mau nambah format HTML, tinggal tambah HtmlReportGenerator() di list ini.
    # Gak perlu ubah kodingan di dalam ReportManager-nya.
    report_manager = ReportManager([
        ExcelReportGenerator(),
        PdfReportGenerator()
    ])
    
    #  STRATEGY PATTERN 
    # Ini inti dari logika penilaian kita. Kita bungkus algoritma penilaian
    # (MCQ, Isian, Essay) jadi object terpisah. Nanti Grader tinggal pilih
    # mau pake strategi yang mana sesuai tipe soal.
    grading_types = {
        "mcq": MCQGradingType(),
        "short_answer": ShortAnswerGradingType(),
        # Essay butuh input manual, jadi kita passing UI ke dia via Interface (ISP)
        "essay": EssayGradingType(ui) 
    }
    
    # Kita pake DebugGrader biar keliatan log-nya di terminal (Liskov Substitution Principle aman di sini).
    grader = DebugGrader(grading_types)

    #  COMPOSITION ROOT 
    # Masukin semua dependencies ke aplikasi utama.
    app = ExamGraderApp(
        ui=ui,
        file_manager=file_manager,
        grader=grader,
        report_manager=report_manager
    )

    app.run()