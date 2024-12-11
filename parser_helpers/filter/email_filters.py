class EmailDomainFilter:
    def __init__(self, website_emails, email_part=None, domain_part=None):
        self.website_emails = website_emails
        self.email_part = email_part
        self.domain_part = domain_part

    def filter_emails(self):
        filtered_data = {}

        for website, emails in self.website_emails.items():
            filtered_emails = set()
            for email in emails:
                local_part, domain = email.split("@")
                if (self.email_part is None or self.email_part in local_part) and (
                    self.domain_part is None or self.domain_part in domain
                ):
                    filtered_emails.add(email)

            if filtered_emails:
                filtered_data[website] = filtered_emails

        self.website_emails = filtered_data
