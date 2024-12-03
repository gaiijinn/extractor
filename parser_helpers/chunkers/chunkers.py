from abc import ABC, abstractmethod


class BaseChunker(ABC):
    @abstractmethod
    def chunk_data(self, data):
        pass


class SimpleChunker(BaseChunker):
    def __init__(self, num_processes):
        self.num_processes = num_processes

    def chunk_data(self, data):
        """Разбивает данные на примерно равные части для каждого процесса."""
        chunk_size = len(data) // self.num_processes
        chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]

        # Если остались лишние элементы, распределяем их по чанкам
        if len(chunks) > self.num_processes:
            extra_data = chunks.pop()
            for i, item in enumerate(extra_data):
                chunks[i % len(chunks)].append(item)

        return chunks


class PercentageChunker(BaseChunker):
    def __init__(self, percentage):
        if not (0 < percentage and percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage = percentage

    def chunk_data(self, data):
        chunk_size = max(1, int(len(data) * (self.percentage / 100)))
        return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
