class EmailDomainFilter:
    def __init__(self, website_emails):
        self.website_emails = website_emails

    def filter_emails(self, email_part=None, domain_part=None):
        filtered_data = {}

        for website, emails in self.website_emails.items():
            filtered_emails = set()
            for email in emails:
                local_part, domain = email.split('@')
                if (email_part is None or email_part in local_part) and (
                    domain_part is None or domain_part in domain
                ):
                    filtered_emails.add(email)

            if filtered_emails:
                filtered_data[website] = filtered_emails

        return filtered_data


website_emails = {
    "example.com": ["user1@example.com", "user2@example.com"],
    "other.com": ["test@other.com", "admin@other.com"]
}

email_filter = EmailDomainFilter(website_emails)

result = email_filter.filter_emails(email_part="user")
print("Filtered by email part:", result)

result = email_filter.filter_emails(domain_part="com")
print("Filtered by domain part:", result)

result = email_filter.filter_emails(email_part="user", domain_part="example.com")
print("Filtered by email part and domain part:", result)