from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser

from parser_helpers.csv_readers import csv_reader
from parser_helpers.fast_parcer.fast_process import BaseFastProcessor


class WebsiteProcessor(BaseFastProcessor):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.browser = kwargs.get("browser", RequestsBrowser)()

    def worker_function(self, data):
        factory = Factory(website_url=data, browser=self.browser, depth=5, max_links_from_page=1)
        worker = DefaultWorker(factory)
        return worker.get_data()


if __name__ == "__main__":
    file = csv_reader.CSVReader(file_path="../crunchbase_data/small_data.csv", row_name="homepage_url")
    websites = file.read_file()

    processor_simple = WebsiteProcessor(data=websites, threads=30, processes=2)
    result_simple = processor_simple.run()
    print(result_simple)
