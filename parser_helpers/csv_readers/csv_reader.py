import csv
from abc import ABC, abstractmethod


class BaseCSVReader(ABC):
    def __init__(self, file_path, row_name):
        self.file_path = file_path
        self.row_name = row_name

    @abstractmethod
    def read_file(self, **kwargs):
        pass


class CSVReader(BaseCSVReader):
    def __init__(self, row_name, file_path):
        super().__init__(file_path, row_name)

    def read_file(self, **kwargs):
        try:
            with open(self.file_path, "r", encoding="utf-8") as infile:
                reader = csv.DictReader(infile)

                if self.row_name not in reader.fieldnames:
                    raise ValueError(f"Column '{self.row_name}' not found in the file.")

                return [row[self.row_name] for row in reader if row.get(self.row_name)]
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.file_path}' not found.")


class CSVMultiReader(BaseCSVReader):
    def __init__(self, row_names, file_path):
        if not isinstance(row_names, list) or not all(isinstance(name, str) for name in row_names):
            raise ValueError("row_names must be a list of strings")
        self.row_names = row_names
        super().__init__(row_name=row_names, file_path=file_path)

    def read_file(self, **kwargs):
        try:
            with open(self.file_path, "r", encoding="utf-8") as infile:
                reader = csv.DictReader(infile)

                missing_columns = [col for col in self.row_names if col not in reader.fieldnames]
                if missing_columns:
                    raise ValueError(f"Columns {missing_columns} not found in the file.")
                return [{col: row.get(col, None) for col in self.row_names} for row in reader]
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.file_path}' not found.")
