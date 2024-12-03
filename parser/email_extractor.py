import subprocess
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from parser_helpers.installer.email_extractor_installer import CurlInstaller


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass


class EmailExtractor(CurlInstaller, BaseEmailExtractor):
    def __init__(self, output_file: str, data, num_threads: int = 100):
        self.output_file = output_file
        self.results = {}
        self._data = data
        self.num_threads = num_threads

    def extract_emails_from_url(self, homepage_url: str) -> list:
        try:
            subprocess.run(
                [
                    "email_extractor",
                    "-depth=1",
                    f"-out={self.output_file}",
                    f"-url={homepage_url}",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with open(self.output_file, mode="r", encoding="utf-8") as f:
                emails = f.read().strip().split("\n")
                print([email for email in emails if email])
                return [email for email in emails if email]
        except subprocess.CalledProcessError as e:
            print(f"Error processing {homepage_url}: {e}")
        return []

    def _process_row(self, row):
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
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            future_to_row = {executor.submit(self._process_row, row): row for row in self._data}

            for future in as_completed(future_to_row):
                row = future_to_row[future]
                try:
                    future.result()  # Retrieve any exceptions here
                except Exception as e:
                    print(f"Error processing row {row}: {e}")

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
