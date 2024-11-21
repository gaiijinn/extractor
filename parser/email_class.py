from abc import ABC, abstractmethod


class BaseEmailExtractor(ABC):
    @abstractmethod
    def install_extractor(self):
        pass

    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass

class BaseEmailSaver(ABC):
    @abstractmethod
    def process_csv(self):
        pass

    @abstractmethod
    def save_results(self, output_path: str):
        pass
