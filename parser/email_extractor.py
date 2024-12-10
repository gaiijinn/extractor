import asyncio
import os
import subprocess
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

import aiofiles

from parser_helpers.csv_readers.csv_reader import CSVMultiReader
from parser_helpers.installer.email_extractor_installer import CurlInstaller


class BaseEmailExtractor(ABC):
    @abstractmethod
    def extract_emails_from_url(self, domain: str) -> list:
        pass


class EmailExtractor:
    def __init__(self, data, num_threads: int = 70):
        self.output_file = "finals/emails_test.csv"
        self.results = {}
        self._data = data
        self.num_threads = num_threads

    async def extract_emails_from_url(self, homepage_url: str) -> list:
        try:
            process = await asyncio.create_subprocess_exec(
                "email_extractor",
                f"-out={self.output_file}",
                f"-url={homepage_url}",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await process.communicate()

            if process.returncode == 0:
                async with aiofiles.open(self.output_file, mode="r", encoding="utf-8") as f:
                    emails = await f.read()
                    return [email for email in emails.strip().split("\n") if email]
        except Exception as e:
            print(f"Error processing {homepage_url}: {e}")
        return []

    async def _process_row(self, row):
        local_results = {}
        uuid = row.get("uuid", "").strip()
        homepage_url = row.get("homepage_url", "").strip()

        if homepage_url:
            print(f"Processing {homepage_url}")
            emails = await self.extract_emails_from_url(homepage_url)
            if emails:
                for email in emails:
                    if uuid in local_results:
                        local_results[uuid].add(email)
                    else:
                        local_results[uuid] = {email}
        return local_results

    async def process_csv(self):
        tasks = []
        for row in self._data:
            tasks.append(self._process_row(row))

        local_results_list = await asyncio.gather(*tasks)

        for local_results in local_results_list:
            for uuid, emails in local_results.items():
                if uuid in self.results:
                    self.results[uuid].update(emails)
                else:
                    self.results[uuid] = emails

    def get_result(self):
        return self.results


# if __name__ == "__main__":
#    input_path = "crunchbase_data/small_data.csv"
#    output_file = "finals/finalemail_extractor.csv"
#
#    parser = CSVMultiReader(["uuid", "homepage_url"], file_path=input_path)
#    rows = parser.read_file()
#
#    extractor = EmailExtractor(output_file=output_file, data=rows)
#    extractor.process_csv()
#    print(extractor.results)
#
