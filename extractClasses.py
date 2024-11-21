import re
from typing import Dict, Set
import csv


class EmailValidator:
    def __init__(self, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"):
        self.pattern = pattern

    def validate(self, email):
        if re.match(self.pattern, email):
            return email
        return None


class RemoveDuplicatesEmails:
    def __init__(self, input_path: str, output_path: str, validator: EmailValidator):
        self.input_path = input_path
        self.output_path = output_path
        self.website_emails: Dict[str, Set[str]] = {}
        self.validator = validator

    def load_emails(self) -> None:
        with open(self.input_path, mode="r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                website = row["website"]
                email = row["email"]

                if not email:
                    continue

                valid_email = self.validator.validate(email)
                if valid_email:
                    if website in self.website_emails:
                        self.website_emails[website].add(valid_email)
                    else:
                        self.website_emails[website] = {valid_email}


    def save_emails_to_csv(self) -> None:
        with open(self.output_path, mode="w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["website", "email"])
            writer.writeheader()

            for website, emails in self.website_emails.items():
                for email in emails:
                    writer.writerow({"website": website, "email": email})

    def start_remove_duplicates_emails(self) -> None:
        self.load_emails()
        self.save_emails_to_csv()