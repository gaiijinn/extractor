import csv
import subprocess
from abc import ABC, abstractmethod
from parser.csv_reader import CSVMultiReader


class BaseEmailExtractor(ABC):
    @abstractmethod
    def install_extractor(self):
        pass

    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass


class EmailExtractor(BaseEmailExtractor):
    def __init__(self, output_path: str):
        self.output_path = output_path

    def install_extractor(self):
        try:
            subprocess.run(
                "curl -sL https://raw.githubusercontent.com/kevincobain2000/email_extractor/master/install.sh | sh",
                shell=True,
                check=True,
            )
            subprocess.run("mv email_extractor /usr/local/bin/", shell=True, check=True)
            print("Installed email_extractor")
        except subprocess.CalledProcessError as e:
            print(f'Error {e}')

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


class BaseEmailSaver(ABC):
    @abstractmethod
    def process_csv(self):
        pass

    @abstractmethod
    def save_results(self, output_path: str):
        pass


class EmailSaver(BaseEmailSaver):
    def __init__(self, email_extractor: BaseEmailExtractor, data: list):
        self.email_extractor = email_extractor
        self.data = data
        self.summary_data = []

    def process_csv(self):
        for row in self.data:
            uuid = row.get('uuid', '').strip()
            homepage_url = row.get('homepage_url', '').strip()

            if homepage_url:
                print(f"Processing {homepage_url}")
                emails = self.email_extractor.extract_emails_from_url(homepage_url)
                if emails:
                    for email in emails:
                        self.summary_data.append({'uuid': uuid, 'extracted_emails': email})
            else:
                print("no homepage_url")

    def save_results(self, output_path: str):
        with open(output_path, mode='w', encoding="utf-8", newline='') as summary_file:
            fieldnames = ['uuid', 'extracted_emails']
            summary_writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            summary_writer.writeheader()
            summary_writer.writerows(self.summary_data)


class EmailFactory:
    def __init__(self, email_extractor: BaseEmailExtractor, email_saver: BaseEmailSaver, output_path: str):
        self.email_extractor = email_extractor
        self.email_saver = email_saver
        self.output_path = output_path

    def run(self):
        self.email_extractor.install_extractor()
        self.email_saver.process_csv()
        self.email_saver.save_results(self.output_path)
        print('Done')


if __name__ == '__main__':
    input_path = '../crunchbase_data/small_data.csv'
    output_path = '../finals/finalemail_extractor.csv'

    parser = CSVMultiReader(['uuid', 'homepage_url'], file_path=input_path)
    rows = parser.read_file()

    email_extractor = EmailExtractor(output_path=output_path)
    email_saver = EmailSaver(email_extractor=email_extractor, data=rows)

    factory = EmailFactory(email_extractor=email_extractor, email_saver=email_saver, output_path=output_path)
    factory.run()
    