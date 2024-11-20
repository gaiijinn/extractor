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