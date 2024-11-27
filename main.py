from parser.email_extractor import EmailExtractor
from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.savers.email_saver import EmailSaver

parser = CSVMultiReader(["uuid", "homepage_url"], file_path='crunchbase_data/small_investors.csv')
rows = parser.read_file()

extractor = EmailExtractor(output_file='finals/investor_email.csv', data=rows)
extractor.process_csv()

emails = extractor.get_result()

saver = EmailSaver(output_file='finals/email.csv', data=emails)
saver.save_result()