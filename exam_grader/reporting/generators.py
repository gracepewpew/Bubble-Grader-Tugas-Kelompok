from abc import ABC, abstractmethod
import pandas as pd
from ..models import StudentResult

class IReportGenerator(ABC):
    @abstractmethod
    def generate(self, results: list[StudentResult], output_path: str):
        pass

class ExcelReportGenerator(IReportGenerator):
    def generate(self, results: list[StudentResult], output_path: str):
        if not results:
            print("No results to generate report.")
            return

        results_data = [res.to_dict() for res in results]
        
        df = pd.DataFrame(results_data)
        
        if not output_path.endswith('.xlsx'):
            output_path += '.xlsx'
            
        df.to_excel(output_path, index=False)
        print(f"Successfully generated Excel report at: {output_path}")

class PdfReportGenerator(IReportGenerator):
    def generate(self, results: list[StudentResult], output_path: str):
        print(f"PDF generation is not yet implemented. Would create PDF at: {output_path}.pdf")