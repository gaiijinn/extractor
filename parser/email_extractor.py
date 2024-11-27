import subprocess
from abc import ABC, abstractmethod

from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.installer.email_extractor_installer import CurlInstaller


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass


class EmailExtractor(CurlInstaller, BaseEmailExtractor):
    def __init__(self, output_file: str, data):
        self.output_file = output_file
        self.results = []
        self._data = data

    def install_extractor(self):
        self.install()

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
                a = [email for email in emails if email]
                print(a)
                return a
        except subprocess.CalledProcessError as e:
            print(f"Error processing {homepage_url}: {e}")
        return []

    def process_csv(self):
        for row in self._data:
            uuid = row.get("uuid", "").strip()
            homepage_url = row.get("homepage_url", "").strip()

            if homepage_url:
                print(f"Processing {homepage_url}")
                emails = self.extract_emails_from_url(homepage_url)
                if emails:
                    for email in emails:
                        self.results.append({"uuid": uuid, "emails": email})

    def get_data(self):
        return self._data


if __name__ == "__main__":
    input_path = "crunchbase_data/small_data.csv"
    output_file = "finals/finalemail_extractor.csv"

    parser = CSVMultiReader(["uuid", "homepage_url"], file_path=input_path)
    rows = parser.read_file()

    extractor = EmailExtractor(output_file=output_file, data=rows)
    extractor.process_csv()
    print(extractor.results)
