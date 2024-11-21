import csv
import subprocess
from parser.csv_reader import CSVReader


class EmailExtractor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.summary_data = []

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
                ["email_extractor", f"-out={self.output_file}", f"-url={domain}"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            with open(output_file, mode="r", encoding="utf-8") as f:
                emails = f.read().strip().split('\n')
                return [email for email in emails if email]
        except subprocess.CalledProcessError as e:
            print(f"Error processing {domain}: {e}")
        return []

    def process_csv(self):
        parser = CSVReader('homepage_url', input_file)
        homepage_urls = parser.read_file()

        for homepage_url in homepage_urls:
            homepage_url = homepage_url.strip()
            if homepage_url:
                print(f"Processing {homepage_url}")
                emails = self.extract_emails_from_url(homepage_url)
                for email in emails:
                    self.summary_data.append({'homepage_url': homepage_url, 'extracted_emails': email})
            else:
                self.summary_data.append({'homepage_url': homepage_url, 'extracted_emails': 'No email found'})

    def save_results(self):
        with open(output_file, mode='w', encoding="utf-8", newline='') as summary_file:
            fieldnames = ['homepage_url', 'extracted_emails']
            summary_writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
            summary_writer.writeheader()
            summary_writer.writerows(self.summary_data)

    def run(self):
        self.process_csv()
        self.save_results()
        print("Done")


if __name__ == '__main__':
    EmailExtractor.install_extractor()
    input_file = 'small_data.csv'
    output_file = 'result_small_data.csv'

    extractor = EmailExtractor(input_file, output_file)
    extractor.run()
