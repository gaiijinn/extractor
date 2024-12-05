import abc
import csv
import re
from typing import Dict, Set


class BaseEmailValidator(abc.ABC):
    def __init__(self, pattern):
        self.pattern = pattern

    @abc.abstractmethod
    def validate(self, **kwargs):
        pass


class EmailValidator(BaseEmailValidator):
    def __init__(self, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"):
        super().__init__(pattern)

    def validate(self, email):
        if re.match(self.pattern, email):
            return email
        return None


class RemoveDuplicatesEmails:
    def __init__(self, input_path: str, output_path: str, validator: EmailValidator = None):
        self.input_path = input_path
        self.output_path = output_path
        self.website_emails: Dict[str, Set[str]] = {}
        self.all_emails: Set[str] = set()
        self.validator = validator or EmailValidator()

    def load_emails(self) -> None:
        with open(self.input_path, mode="r", encoding="utf-8", newline="") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                uuid = row["uuid"]
                email = row["email"]

                if not email:
                    continue

                valid_email = self.validator.validate(email)
                if valid_email:
                    if valid_email in self.all_emails:
                        continue

                    self.all_emails.add(valid_email)

                    if uuid in self.website_emails:
                        self.website_emails[uuid].add(valid_email)
                    else:
                        self.website_emails[uuid] = {valid_email}

    def save_emails_to_csv(self) -> None:
        with open(self.output_path, mode="w", encoding="utf-8", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=["uuid", "email"])
            writer.writeheader()

            for uuid, emails in self.website_emails.items():
                for email in emails:
                    writer.writerow({"uuid": uuid, "email": email})

    def start_remove_duplicates_emails(self) -> None:
        self.load_emails()
        self.save_emails_to_csv()
