import csv
import subprocess
from parser.csv_reader import CSVMultiReader


class EmailExtractor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    @staticmethod
    def install_extractor():
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

    def extract_emails_from_url(self, domain):
        try:
            subprocess.run(
                ["email_extractor", f"-out={self.output_path}", f"-url={domain}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with open(output_path, mode="r", encoding="utf-8") as f:
                emails = f.read().strip().split('\n')
                print(emails)
                return [email for email in emails if email]
        except subprocess.CalledProcessError as e:
            print(f"Error processing {domain}: {e}")
        return []


class EmailSaver:
    def __init__(self, input_path, output_path, data):
        self.email_extractor = EmailExtractor(input_path, output_path)
        self.summary_data = []
        self.data = data

    def process_csv(self):
        for row in self.data:
            uuid = row.get('uuid', '').strip()
            homepage_url = row.get('homepage_url', '').strip()

            if homepage_url:
                print(f"Processing {homepage_url}")
                emails = self.email_extractor.extract_emails_from_url(homepage_url)
                if emails:
                    print('few emails', emails)
                    for email in emails:
                        self.summary_data.append({'uuid': uuid, 'extracted_emails': email})
            else:
                print("no homepage_url")

    def save_results(self):
        with open(output_path, mode='w', encoding="utf-8", newline='') as summary_file:
            fieldnames = ['uuid', 'extracted_emails']
            summary_writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            summary_writer.writeheader()
            summary_writer.writerows(self.summary_data)


class EmailFactory:
    def __init__(self, input_path, output_path, data):
        self.input_path = input_path
        self.output_path = output_path
        self.data = data

        self.email_extractor = EmailExtractor(input_path, output_path)
        self.email_saver = EmailSaver(input_path, output_path, data)

    def run(self):
        self.email_extractor.install_extractor()
        self.email_saver.process_csv()
        self.email_saver.save_results()
        print('Done')


if __name__ == '__main__':
    input_path = '../crunchbase_data/small_data.csv'
    output_path = '../finals/finalemail_extractor.csv'

    parser = CSVMultiReader(['uuid', 'homepage_url'], file_path=input_path)
    rows = parser.read_file()
    print(rows)


    extractor = EmailFactory(input_path, output_path, data=rows)
    extractor.run()
    