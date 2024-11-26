import concurrent.futures
from abc import ABC, abstractmethod
from typing import Type

from parser_helpers.chunkers import chunkers
from parser_helpers.mixins import mixins


class BaseFastProcessor(ABC, mixins.ThreadMixin, mixins.ProcessMixin):
    def __init__(
        self,
        data,
        threads: int = 1,
        processes: int = 1,
        chunker_class: Type[chunkers.BaseChunker] = None,
        **kwargs
    ):
        self.data = data
        self.threads = threads
        self.processes = processes
        self.extra_args = kwargs

        self.chunker = chunker_class or chunkers.SimpleChunker(processes)

    @abstractmethod
    def worker_function(self, item):
        pass

    def process_data(self):
        chunks = self.chunker.chunk_data(self.data)
        results = self.process_in_processes(chunks, self._process_chunk, max_processes=self.processes)
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
