import csv
from typing import Type
from abc import abstractmethod, ABC


class BaseCSVReader(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def read_file(self, **kwargs):
        pass


class CSVReader(BaseCSVReader):
    def __init__(self, row_name, file_path):
        super().__init__(file_path)
        self.row_name = row_name

    def read_file(self, **kwargs):
        with open(self.file_path, "r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            result = list(row[self.row_name] for row in reader if row.get(self.row_name))
            return result


class CSVParser:
    def __init__(self, file_path, row_name, reader_class: Type[BaseCSVReader] = CSVReader):
        self._reader = reader_class(row_name, file_path)

    def get_data(self):
        return self._reader.read_file()
