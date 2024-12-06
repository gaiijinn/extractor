import os
import subprocess
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.installer.email_extractor_installer import CurlInstaller


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass


class EmailExtractor(CurlInstaller, BaseEmailExtractor):
    def __init__(self, data, num_threads: int = 40):
        self.output_file = "finals/emails_test.csv"
        self.results = {}
        self._data = data
        self.num_threads = num_threads

    def extract_emails_from_url(self, homepage_url: str) -> list:
        try:
            subprocess.run(
                [
                    "email_extractor",
                    f"-out={self.output_file}",
                    f"-url={homepage_url}",
                ],
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

    def _process_row(self, row):
        local_results = {}
        uuid = row.get("uuid", "").strip()
        homepage_url = row.get("homepage_url", "").strip()

        if homepage_url:
            print(f"Processing {homepage_url}")
            emails = self.extract_emails_from_url(homepage_url)
            if emails:
                for email in emails:
                    if uuid in local_results:
                        local_results[uuid].add(email)
                    else:
                        local_results[uuid] = {email}
        return local_results

    def process_csv(self):
        local_results_list = []
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_row = {executor.submit(self._process_row, row): row for row in self._data}

            for future in as_completed(future_to_row):
                try:
                    local_results = future.result()
                    local_results_list.append(local_results)
                except Exception as e:
                    row = future_to_row[future]
                    print(f"Error processing row {row}: {e}")

        for local_results in local_results_list:
            for uuid, emails in local_results.items():
                if uuid in self.results:
                    self.results[uuid].update(emails)
                else:
                    self.results[uuid] = emails

    def get_result(self):
        return self.results


# if __name__ == "__main__":
#    input_path = "crunchbase_data/small_data.csv"
#    output_file = "finals/finalemail_extractor.csv"
#
#    parser = CSVMultiReader(["uuid", "homepage_url"], file_path=input_path)
#    rows = parser.read_file()
#
#    extractor = EmailExtractor(output_file=output_file, data=rows)
#    extractor.process_csv()
#    print(extractor.results)
#
