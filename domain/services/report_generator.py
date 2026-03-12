from abc import ABC, abstractmethod
import csv
import pandas as pd


class BaseReportGenerator(ABC):
    @abstractmethod
    def generate(self, data: list[dict], file_path):
        pass


    def _validate_data(self, data):
        if not (data and isinstance(data, list) and all(isinstance(row, dict) for row in data)):
            raise ValueError('It must be list[dict] to save as file')


class CSVReportGenerator(BaseReportGenerator):
    def generate(self, data: list[dict], file_path):
        self._validate_data(data)
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)



class ExcelReportGenerator(BaseReportGenerator):
    def generate(self, data: list[dict], file_path):
        self._validate_data(data)
        
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)