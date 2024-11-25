import re
from typing import Dict, Set
import csv
import abc


class EmailProcessorInterface(abc.ABC):
    @abc.abstractmethod
    def load_emails(self) -> None:
        pass

    @abc.abstractmethod
    def save_emails_to_csv(self) -> None:
        pass

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


class RemoveDuplicatesEmails(EmailProcessorInterface):
    def __init__(self, input_path: str, output_path: str, validator: EmailValidator = None):
        self.input_path = input_path
        self.output_path = output_path
        self.website_emails: Dict[str, Set[str]] = {}
        self.validator = validator or EmailValidator()

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


class EmailDomainFilter(RemoveDuplicatesEmails):
    def filter_emails(self, email_part: str = None, domain_part: str = None) -> dict:
        filtered_data = {}

        for website, emails in self.website_emails.items():
            filtered_emails = set()
            for email in emails:
                local_part, domain = email.split("@")
                if (
                    (email_part is None or email_part in local_part) and
                    (domain_part is None or domain_part in domain)
                ):
                    filtered_emails.add(email)

            if filtered_emails:
                filtered_data[website] = filtered_emails

        self.website_emails = filtered_data


# test = RemoveDuplicatesEmails(input_path='thread_result/just_all_data_2procc_20thread_5depth.csv',
#                               output_path='final_test.csv',)
#
# test.start_remove_duplicates_emails()
# my_data = test.website_emails
# print(my_data)

email_filter = EmailDomainFilter(input_path='final_test.csv', output_path='final_test2.csv')
email_filter.load_emails()
filtered_emails = email_filter.filter_emails(email_part="support", domain_part="gmail.com")
# filtered_emails = email_filter.filter_emails(domain_part="gmail.com")
# filtered_emails = email_filter.filter_emails(email_part="support")
email_filter.save_emails_to_csv()