import csv
from abc import ABC, abstractmethod


class BaseEmailSaver(ABC):
    def __init__(self, output_file: str, data):
        self.output_file = output_file
        self._data = data

    @abstractmethod
    def save_result(self):
        pass


class EmailSaver(BaseEmailSaver):
    def __init__(self, output_file: str, data):
        super().__init__(output_file, data)

    def save_result(self):
        fieldnames = ["uuid", "emails"]

        with open(self.output_file, "w", newline="", encoding="utf-8") as summary_file:
            writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            writer.writeheader()

            for k, v in self._data.items():
                for email in v:
                    writer.writerow({"uuid": k, "emails": email})
