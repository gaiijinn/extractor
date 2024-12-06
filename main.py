from parser.email_extractor import EmailExtractor

from parser_helpers.cleaners.email_cleaner import RemoveDuplicatesEmails
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.savers.email_saver import EmailSaver

if __name__ == "__main__":
    parser = CSVMultiReader(["uuid", "homepage_url"], file_path="crunchbase_data/test.csv")
    rows = parser.read_file()

    extractor = EmailExtractor(data=rows)
    extractor.process_csv()

    emails = extractor.get_result()

    remover = RemoveDuplicatesEmails(emails)
    data = remover.remove_duplicates()

    saver = EmailSaver(output_file="finals/email.csv", data=data)
    saver.save_result()
