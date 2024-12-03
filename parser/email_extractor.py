import os
import subprocess
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List

from parser_helpers.chunkers.chunkers import SimpleChunker
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.installer.email_extractor_installer import CurlInstaller


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, homepage_url: str) -> List[str]:
        pass


class EmailExtractor(CurlInstaller, BaseEmailExtractor):
    def __init__(
        self,
        data,
        output_file: str = Path(__file__).parent.resolve() / "../finals/finalemail_extractor.csv",
        max_threads: int = 100,
        max_processes: int = 4,
    ):
        self.output_file = output_file
        self.results = {}
        self._data = data
        self.max_threads = max_threads
        self.max_processes = max_processes
        self.chunk_object = SimpleChunker(num_processes=self.max_processes)

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

    def process_row(self, row, results):
        uuid = row.get("uuid", "").strip()
        homepage_url = row.get("homepage_url", "").strip()

        if homepage_url:
            print(f"Processing {homepage_url}")
            emails = self.extract_emails_from_url(homepage_url)
            if emails:
                for email in emails:
                    if uuid in results:
                        results[uuid].add(email)
                    else:
                        results[uuid] = {email}

    def process_chunk(self, chunk):
        local_results = {}
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_row = {executor.submit(self.process_row, row, local_results): row for row in chunk}

            for future in as_completed(future_to_row):
                try:
                    future.result()
                except Exception as exc:
                    print(f"Error processing row {future_to_row[future]}: {exc}")
        return local_results

    def process_csv(self):
        chunks = self.chunk_object.chunk_data(self._data)

        with ProcessPoolExecutor(max_workers=self.max_processes) as executor:
            future_to_chunk = {executor.submit(self.process_chunk, chunk): chunk for chunk in chunks}

            for future in as_completed(future_to_chunk):
                try:
                    local_results = future.result()
                    for uuid, emails in local_results.items():
                        if uuid in self.results:
                            self.results[uuid].update(emails)
                        else:
                            self.results[uuid] = set(emails)
                except Exception as exc:
                    print(f"Error processing chunk: {exc}")

    def delete_useless_file(self):
        try:
            if os.path.exists(self.output_file):
                os.remove(self.output_file)
        except Exception as e:
            print(f"Error deleting file {self.output_file}: {e}")

    def get_result(self):
        return self.results


# if __name__ == "__main__":
#     input_path = "../crunchbase_data/small_data.csv"
#     parser = CSVMultiReader(["uuid", "homepage_url"], file_path=input_path)
#     rows = parser.read_file()
#
#     extractor = EmailExtractor(data=rows)
#     extractor.process_csv()
#     results = extractor.get_result()
