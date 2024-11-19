from csv_reader import CSVParser

from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser as Browser
import concurrent.futures
import time
from abc import abstractmethod, ABC



class BaseChunker(ABC):
    @abstractmethod
    def chunk_data(self, data):
        pass

class SimpleChunker(BaseChunker):
    def __init__(self, num_processes):
        self.num_processes = num_processes

    def chunk_data(self, data):
        chunk_size = len(data) // self.num_processes
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


class PercentageChunker(BaseChunker):
    def __init__(self, percentage):
        if not (0 < percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage = percentage

    def chunk_data(self, data):
        chunk_size = max(1, int(len(data) * (self.percentage / 100)))
        return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


class FastParsing:
    def __init__(self, websites, threads=1, process=1):
        self.threads = threads
        self.processes = process
        self.websites = websites
        self.browser = Browser()

    def process_website(self, website):
        factory = Factory(website_url=website, browser=self.browser, depth=5, max_links_from_page=1)
        worker = DefaultWorker(factory)
        return worker.get_data()

    def process_websites_in_thread(self, websites_chunk):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as thread_executor:
            futures = [thread_executor.submit(self.process_website, website) for website in websites_chunk]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

    def processing(self):
        start_time = time.time()

        chunker = SimpleChunker(self.processes)
        website_chunks = chunker.chunk_data(self.websites)

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.processes) as process_executor:
            futures = [
                process_executor.submit(self.process_websites_in_thread, chunk) for chunk in website_chunks
            ]
            all_data = []
            for future in concurrent.futures.as_completed(futures):
                all_data.extend(future.result())

        for data in all_data:
            print(data)

        end_time = time.time()
        print(f"Total processing time: {end_time - start_time:.2f} seconds")


if __name__ == '__main__':
    file = CSVParser(file_path='crunchbase_data/organizations.csv', row_name='homepage_url')
    res = file.get_data()
    fast = FastParsing(websites=res, threads=80, process=3)
    fast.processing()