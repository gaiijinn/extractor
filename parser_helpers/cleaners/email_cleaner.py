import abc
import re
from typing import Dict, Set


class BaseEmailValidator(abc.ABC):
    def __init__(self, pattern):
        self.pattern = pattern

    @abc.abstractmethod
    def validate(self, **kwargs):
        pass


class EmailValidator:
    def __init__(self, pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"):
        self.pattern = pattern

    def validate(self, email):
        if re.match(self.pattern, email):
            return email
        return None


class RemoveDuplicatesEmails:
    def __init__(self, website_emails, validator: EmailValidator = None):
        self.website_emails: Dict[str, Set[str]] = website_emails
        self.all_emails: Set[str] = set()
        self.validator = validator or EmailValidator()

    async def remove_duplicates(self):
        local_emails = {}

        for key, value in self.website_emails.items():
            for email in value:
                if not email:
                    continue

                valid_email = self.validator.validate(email)

                if valid_email:
                    if valid_email in self.all_emails:
                        continue

                    self.all_emails.add(valid_email)

                    if key in local_emails:
                        local_emails[key].add(valid_email)
                    else:
                        local_emails[key] = {valid_email}

        return local_emails
