import csv
import subprocess
from typing import Type
from parser.csv_reader import CSVMultiReader
from email_class import BaseEmailExtractor, BaseEmailSaver, BaseInstaller, CurlInstaller


class EmailExtractor(BaseEmailExtractor, BaseInstaller):
    def __init__(self, output_path: str):
        self.output_path = output_path

    def install_extractor(self):
        self.install()

    def extract_emails_from_url(self, domain: str) -> list:
        try:
            subprocess.run(
                ["email_extractor", f"-out={self.output_path}", f"-url={domain}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with open(output_path, mode="r", encoding="utf-8") as f:
                emails = f.read().strip().split('\n')
                return [email for email in emails if email]
        except subprocess.CalledProcessError as e:
            print(f"Error processing {domain}: {e}")
        return []


class EmailSaver(BaseEmailSaver):
    def __init__(self, email_extractor: BaseEmailExtractor, data: list):
        self.email_extractor = email_extractor
        self.data = data
        self.results = []

    def process_csv(self):
        for row in self.data:
            uuid = row.get('uuid', '').strip()
            homepage_url = row.get('homepage_url', '').strip()

            if homepage_url:
                print(f"Processing {homepage_url}")
                emails = self.email_extractor.extract_emails_from_url(homepage_url)
                if emails:
                    for email in emails:
                        self.results.append({"uuid": uuid, "emails": email})
                else:
                    self.results.append({"uuid": uuid, "emails": None})
            else:
                self.results.append({"uuid": uuid, "emails": None})

    def save_results(self, output_path: str):
        fieldnames = ['uuid', 'emails']

        with open(output_path, mode='w', encoding="utf-8", newline='') as summary_file:
            summary_writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            summary_writer.writeheader()

            for result in self.results:
                summary_writer.writerow(result)

class EmailFactory:
    def __init__(
            self,
            email_extractor_class: Type[BaseEmailExtractor],
            email_saver_class: Type[BaseEmailSaver],
            installer_class: Type[BaseInstaller],
            output_path: str,
            data: list
    ):
        self.email_extractor = email_extractor_class(output_path, installer_class())
        self.email_saver = email_saver_class(self.email_extractor, data)
        self.output_path = output_path

    def run(self):
        self.email_extractor.install_extractor()
        self.email_saver.process_csv()
        self.email_saver.save_results(self.output_path)


if __name__ == '__main__':
    input_path = '../crunchbase_data/small_data.csv'
    output_path = '../finals/finalemail_extractor.csv'

    parser = CSVMultiReader(['uuid', 'homepage_url'], file_path=input_path)
    rows = parser.read_file()

    factory = EmailFactory(
        email_extractor_class=EmailExtractor,
        email_saver_class=EmailSaver,
        installer_class=CurlInstaller,
        output_path=output_path,
        data=rows
    )

    factory.run()

