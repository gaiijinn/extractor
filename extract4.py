import csv
import time
import concurrent.futures
from pathlib import Path
from extract_emails import DefaultFilterAndEmailFactory as Factory
from extract_emails import DefaultWorker
from extract_emails.browsers.requests_browser import RequestsBrowser as Browser

def read_websites(file_path):
    with open(file_path, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        result = list(row["homepage_url"] for row in reader if row.get("homepage_url"))
        return result

def save_to_custom_csv(data, output_path):
    with open(output_path, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(["website", "page", "email"])

        for row in data:
            website = getattr(row, 'website', '')
            page = getattr(row, 'page', '')
            email = ''
            if hasattr(row, 'data') and 'email' in row.data:
                email_list = row.data['email']
                if email_list:
                    email = email_list[0]

            writer.writerow([website, page, email])

def process_website(website, browser):
    factory = Factory(
        website_url=website, browser=browser, depth=5, max_links_from_page=1
    )
    worker = DefaultWorker(factory)
    data = worker.get_data()
    return data

def process_websites_in_process(websites, browser):
    with concurrent.futures.ThreadPoolExecutor(max_workers=70) as thread_executor:
        futures = [thread_executor.submit(process_website, website, browser) for website in websites]
        all_data = [future.result() for future in concurrent.futures.as_completed(futures)]
    return all_data

def remove_duplicates_and_empty_emails(input_path, output_path):
    seen = set()

    with open(input_path, mode="r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            email = row["email"]
            if email:
                seen.add((row["website"], email))

    with open(output_path, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["website", "email"])
        writer.writeheader()
        writer.writerows({"website": website, "email": email} for website, email in seen)


def main():
    time_start = time.time()
    browser = Browser()
    output_path = Path("thread_result/just_all_data_3procc_70thread_5depth2.csv")
    final_output_path = Path("thread_result/just_all_data_filtered2.csv")

    websites = read_websites('crunchbase_data/organizations1.csv')
    # websites = read_websites('crunchbase_data/test.csv')

    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as process_executor:
        chunk_size = len(websites) // 3
        website_chunks = [websites[i:i + chunk_size] for i in range(0, len(websites), chunk_size)]

        futures = [process_executor.submit(process_websites_in_process, chunk, browser) for chunk in website_chunks]

        all_data = []
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            all_data.extend(data)

        for data in all_data:
            save_to_custom_csv(data, output_path)

    remove_duplicates_and_empty_emails(output_path, final_output_path)

    time_end = time.time()
    print(f"Processing time: {time_end - time_start:.2f} seconds")

if __name__ == "__main__":
    main()
