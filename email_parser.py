from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser
import concurrent.futures
from typing import Type
from parser import chunkers, mixins, csv_reader
import abc



class BaseFastProcessor(abc.ABC, mixins.ThreadMixin, mixins.ProcessMixin):
    def __init__(self, data, threads: int = 1, processes: int = 1,
                 chunker_class: Type[chunkers.BaseChunker] = chunkers.SimpleChunker,
                 **kwargs):
        self.data = data
        self.threads = threads
        self.processes = processes
        self.chunker = chunker_class(self.processes)
        self.extra_args = kwargs

    @abc.abstractmethod
    def worker_function(self, item):
        pass

    def process_data(self):
        chunks = self.chunker.chunk_data(self.data)
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

    def run(self):
        return self.process_data()


class WebsiteProcessor(BaseFastProcessor):
    def __init__(self, websites, **kwargs):
        super().__init__(websites, **kwargs)
        self.browser = kwargs.get("browser", RequestsBrowser)()

    def worker_function(self, website):
        factory = Factory(website_url=website, browser=self.browser, depth=5, max_links_from_page=1)
        worker = DefaultWorker(factory)
        return worker.get_data()



if __name__ == '__main__':
    file = csv_reader.CSVReader(file_path='crunchbase_data/small_data.csv', row_name='homepage_url')
    websites = file.read_file()

    processor_simple = WebsiteProcessor(websites=websites, threads=30, processes=2)
    result_simple = processor_simple.run()
    print(result_simple)