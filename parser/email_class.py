import subprocess
from abc import ABC, abstractmethod


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass

class BaseInstaller:
    def install(self):
        raise NotImplementedError("Install method must be implemented")

class CurlInstaller(BaseInstaller):
    def install(self):
        try:
            subprocess.run(
                "curl -sL https://raw.githubusercontent.com/kevincobain2000/email_extractor/master/install.sh | sh",
                shell=True,
                check=True,
            )
            subprocess.run("mv email_extractor /usr/local/bin/", shell=True, check=True)
            print("Installed email_extractor")
        except subprocess.CalledProcessError as e:
            print(f"Error during installation: {e}")

class BaseEmailSaver(ABC):
    @abstractmethod
    def process_csv(self):
        pass

    @abstractmethod
    def save_results(self, output_path: str):
        pass
