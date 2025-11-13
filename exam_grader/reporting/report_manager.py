from .generators import IReportGenerator, ExcelReportGenerator, PdfReportGenerator
from ..models import StudentResult

class ReportManager:
    def __init__(self):
        self._generators: list[IReportGenerator] = [
            ExcelReportGenerator(),
            PdfReportGenerator()
        ]

    def generate_all_reports(self, results: list[StudentResult], class_name: str):
        print("\n--- Generating Reports ---")
        base_filename = f"output/{class_name}_Report"
        for generator in self._generators:
            generator.generate(results, base_filename)