from parser.csv_reader import CSVParser
from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser
import concurrent.futures
import time
from extract_emails.browsers.page_source_getter import PageSourceGetter
from typing import Type
from parser import chunkers, mixins
import abc


class BaseFastProcessor(abc.ABC, mixins.ThreadMixin, mixins.ProcessMixin):
    def __init__(self, threads: int = 1, processes: int = 1,
                 chunker_class: Type[chunkers.BaseChunker] = chunkers.SimpleChunker):
        self.threads = threads
        self.processes = processes
        self.chunker = chunker_class(self.processes)

    @abc.abstractmethod
    def worker_function(self, item):
        pass

    def process_data(self, data):
        chunks = self.chunker.chunk_data(data)
        results = self.process_in_processes(
            chunks, self._process_chunk, max_processes=self.processes
        )
        return [item for sublist in results for item in sublist]

    def process_in_threads(self, items, worker_func, max_threads):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(worker_func, item) for item in items]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

    def process_in_processes(self, items, worker_func, max_processes):
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_processes) as executor:
            futures = [executor.submit(worker_func, item) for item in items]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

    def _process_chunk(self, chunk):
        return self.process_in_threads(chunk, self.worker_function, max_threads=self.threads)


class WebsiteProcessor(BaseFastProcessor):
    def __init__(self, websites, threads: int = 1, processes: int = 1,
                 chunker_class: Type[chunkers.BaseChunker] = chunkers.SimpleChunker,
                 browser: Type[PageSourceGetter] = RequestsBrowser):
        super().__init__(threads, processes, chunker_class)
        self.websites = websites
        self.browser = browser()

    def worker_function(self, website):
        factory = Factory(website_url=website, browser=self.browser, depth=5, max_links_from_page=1)
        worker = DefaultWorker(factory)
        return worker.get_data()

    def run(self):
        return self.process_data(self.websites)


if __name__ == '__main__':
    file = CSVParser(file_path='crunchbase_data/test.csv', row_name='homepage_url')
    websites = file.get_data()

    time_start = time.time()
    processor_simple = WebsiteProcessor(websites=websites, threads=70, processes=3)
    result_simple = processor_simple.run()
    time_end = time.time()
    print(result_simple)
    print(time_end-time_start)
    print(len(result_simple))