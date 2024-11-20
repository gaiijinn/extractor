import csv
import subprocess


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
    with open(input_file, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            homepage_url = row.get("homepage_url", "").strip()
            if homepage_url:
                print(f"Обрабатывается: {homepage_url}")
                emails = extract_emails_from_url(homepage_url, output_file)
                for email in emails:
                    summary_data.append({"domain": homepage_url, "extracted_emails": email})
            else:
                summary_data.append({"domain": homepage_url, "extracted_emails": "No emails found"})
    with open(output_file, mode="w", encoding="utf-8", newline="") as summary_outfile:
        fieldnames = ["domain", "extracted_emails"]
        summary_writer = csv.DictWriter(summary_outfile, fieldnames=fieldnames)
        summary_writer.writeheader()
        summary_writer.writerows(summary_data)


if __name__ == '__main__':
    install_extractor()
    input_file = 'small_data.csv'
    output_file = 'result.csv'
    process_csv(input_file, output_file)
    print('Done!')
