import csv
import subprocess
from typing import Type
from parser.csv_reader import CSVMultiReader
from email_class import BaseEmailExtractor, BaseEmailSaver, CurlInstaller, BaseInstaller


class EmailExtractor(CurlInstaller, BaseEmailExtractor):
    def __init__(self, output_file: str):
        self.output_file = output_file

    def install_extractor(self):
        self.install()

    def extract_emails_from_url(self, homepage_url: str) -> list:
        try:
            subprocess.run(
                ["email_extractor", f"-out={self.output_file}", f"-url={homepage_url}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with open(output_file, mode="r", encoding="utf-8") as f:
                emails = f.read().strip().split('\n')
                return [email for email in emails if email]
        except subprocess.CalledProcessError as e:
            print(f"Error processing {homepage_url}: {e}")
        return []


class EmailSaver(BaseEmailSaver):
    def __init__(self,
                 data: list,
                 email_extractor_class: Type[BaseEmailExtractor] = None
                 ):
        self.email_extractor = email_extractor_class or EmailExtractor(output_file)
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

    def save_results(self, output_file: str):
        fieldnames = ['uuid', 'emails']

        with open(output_file, mode='w', encoding="utf-8", newline='') as summary_file:
            summary_writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            summary_writer.writeheader()

            for result in self.results:
                summary_writer.writerow(result)

class EmailFactory:
    def __init__(
            self,
            output_file: str,
            data: list,
            email_extractor_class: Type[BaseEmailExtractor] = None ,
            email_saver_class: Type[BaseEmailSaver] = None,
            installer_class: Type[BaseInstaller] = None,
    ):
        self.email_extractor = email_extractor_class or EmailExtractor(output_file)
        self.email_saver = email_saver_class or EmailSaver(data)
        self.installer = installer_class or CurlInstaller()
        self.output_file = output_file

    def run(self):
        self.email_extractor.install_extractor()
        self.email_saver.process_csv()
        self.email_saver.save_results(self.output_file)


if __name__ == '__main__':
    input_path = '../crunchbase_data/small_data.csv.csv'
    output_file = '../finals/finalemail_extractor.csv'

    parser = CSVMultiReader(['uuid', 'homepage_url'], file_path=input_path)
    rows = parser.read_file()

    print()
    factory = EmailFactory(
        output_file=output_file,
        data=rows,
    )

    factory.run()

