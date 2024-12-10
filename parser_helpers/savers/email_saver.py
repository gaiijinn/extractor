import csv
from abc import ABC, abstractmethod

import aiofiles


class BaseEmailSaver(ABC):
    def __init__(self, output_file: str, data):
        self.output_file = output_file
        self._data = data

    @abstractmethod
    def save_result(self):
        pass


class EmailSaver:
    def __init__(self, output_file: str, data):
        self.output_file = output_file
        self._data = data

    async def save_result(self):
        fieldnames = ["uuid", "emails"]

        async with aiofiles.open(self.output_file, mode="w", encoding="utf-8") as summary_file:
            writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            await summary_file.write(",".join(fieldnames) + "\n")  # Write header

            for k, v in self._data.items():
                for email in v:
                    await summary_file.write(f"{k},{email}\n")
