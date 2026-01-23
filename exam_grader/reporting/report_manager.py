from .generators import IReportGenerator
from ..models import StudentResult

class ReportManager:
    def __init__(self, generators: list[IReportGenerator] = None):
        self._generators = generators if generators else []

    def add_generator(self, generator: IReportGenerator):
        self._generators.append(generator)

    def generate_all_reports(self, results: list[StudentResult], class_name: str):
        if not self._generators:
            print("Warning: No report generators registered.")
            return

        print("\n Generating Reports")
        base_filename = f"output/{class_name}_Report"
        for generator in self._generators:
            generator.generate(results, base_filename)