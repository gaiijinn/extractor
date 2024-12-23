import subprocess
from abc import ABC, abstractmethod


class BaseInstaller(ABC):
    @abstractmethod
    def install(self):
        pass


class CurlInstaller(BaseInstaller):
    def install(self):
        try:
            subprocess.run(
                [
                    "curl",
                    "-sL",
                    "https://raw.githubusercontent.com/kevincobain2000/email_extractor/master/install.sh",
                ],
                check=True,
                shell=False,
            )
            subprocess.run(
                ["mv", "email_extractor", "/usr/local/bin/"],
                check=True,
                shell=False,
            )
            print("Installed email_extractor")
        except subprocess.CalledProcessError as e:
            print(f"Error during installation: {e}")
