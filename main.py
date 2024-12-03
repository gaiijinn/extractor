from parser.email_extractor import EmailExtractor

from parser_helpers.cleaners.email_cleaner import RemoveDuplicatesEmails
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.savers.email_saver import EmailSaver

if __name__ == "__main__":
    parser = CSVMultiReader(["uuid", "homepage_url"], file_path="crunchbase_data/test.csv")
    rows = parser.read_file()

    extractor = EmailExtractor(output_file="finals/investor_email.csv", data=rows)
    extractor.process_csv()

    emails = extractor.get_result()

    saver = EmailSaver(output_file="finals/email.csv", data=emails)
    saver.save_result()

    # cleaner = RemoveDuplicatesEmails(input_path="finals/email.csv", output_path='finals/cleans.csv')
    # cleaner.start_remove_duplicates_emails()
