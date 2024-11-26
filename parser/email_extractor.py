import subprocess
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.installer.email_extractor_installer import CurlInstaller


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass


class EmailExtractor(CurlInstaller, BaseEmailExtractor):
    def __init__(self, data, output_file: str = "finalemail_extractor.csv", max_threads: int = 70):
        self.output_file = output_file
        self.results = {}
        self._data = data
        self.max_threads = max_threads

        self.install_extractor()

    def install_extractor(self):
        self.install()

    def extract_emails_from_url(self, homepage_url: str) -> List[str]:
        try:
            subprocess.run(
                ["curl, " "email_extractor", "-depth=1", f"-out={self.output_file}", f"-url={homepage_url}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with open(self.output_file, mode="r", encoding="utf-8") as f:
                emails = f.read().strip().split("\n")
                return [email for email in emails if email]
        except subprocess.CalledProcessError as e:
            print(f"Error processing {homepage_url}: {e}")
        return []

    def process_row(self, row):
        uuid = row.get("uuid", "").strip()
        homepage_url = row.get("homepage_url", "").strip()

        if homepage_url:
            print(f"Processing {homepage_url}")
            emails = self.extract_emails_from_url(homepage_url)
            if emails:
                for email in emails:
                    if uuid in self.results:
                        self.results[uuid].add(email)
                    else:
                        self.results[uuid] = {email}

    def process_csv(self):
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_row = {executor.submit(self.process_row, row): row for row in self._data}

            for future in as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"Error processing row {row}: {exc}")

    def get_result(self):
        return self.results


# if __name__ == "__main__":
#
#     input_path = "../crunchbase_data/test.csv"
#     parser = CSVMultiReader(["uuid", "homepage_url"], file_path=input_path)
#     rows = parser.read_file()
#
#     extractor = EmailExtractor(data=rows)
#     extractor.process_csv()
