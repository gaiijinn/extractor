import concurrent.futures
from typing import List


class ThreadMixin:
    def process_in_threads(self, items: List, worker_func, max_threads: int):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(worker_func, item) for item in items]
            return [future.result() for future in concurrent.futures.as_completed(futures)]


class ProcessMixin:
    def process_in_processes(self, items: List, worker_func, max_processes: int):
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_processes) as executor:
            futures = [executor.submit(worker_func, item) for item in items]
            return [future.result() for future in concurrent.futures.as_completed(futures)]
