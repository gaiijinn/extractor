from parser_helpers.cleaners.email_cleaner import RemoveDuplicatesEmails


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