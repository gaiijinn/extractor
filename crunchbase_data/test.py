import csv
import subprocess
from parser.csv_reader import CSVReader


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


def extract_emails_from_url(domain, output_file):
    try:
        subprocess.run(
            ["email_extractor", f"-out={output_file}", f"-url={domain}"],
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


def process_csv(input_file, output_file):
    summary_data = []

    parser = CSVReader('homepage_url', input_file)
    homepage_urls = parser.read_file()

    for homepage_url in homepage_urls:
        homepage_url = homepage_url.strip()
        if homepage_url:
            print(f"Processing {homepage_url}")
            emails = extract_emails_from_url(homepage_url, output_file)
            for email in emails:
                summary_data.append({'homepage_url': homepage_url, 'extracted_emails': email})
        else:
            summary_data.append({'homepage_url': homepage_url, 'extracted_emails': 'No email found'})

    with open(output_file, mode='w', encoding="utf-8", newline='') as summary_file:
        fieldnames = ['homepage_url', 'extracted_emails']
        summary_writer = csv.DictWriter(summary_file, fieldnames=fieldnames)
        summary_writer.writeheader()
        summary_writer.writerows(summary_data)


if __name__ == '__main__':
    install_extractor()
    input_file = 'small_data.csv'
    output_file = 'result_small_data.csv'
    process_csv(input_file, output_file)
    print('Done!')
