from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import re

class CustomScraper:
    def __init__(self, **kwargs):
        self.browser_prefs = kwargs.get("browser_prefs", {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "profile.managed_default_content_settings.fonts": 2,
            "profile.default_content_setting_values.notifications": 2,
        })
        self.ua = UserAgent().random

    def scrape(self, page_url):
        phone_pattern = r'\+?\d[\d\s\-\(\)]{6,}'
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("prefs", self.browser_prefs)
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"user-agent={self.ua}")

        driver = webdriver.Chrome(options=chrome_options)
        try:
            status = 0
            while status != 10:
                try:
                    driver.get(page_url)
                    about_section = driver.find_element(By.CSS_SELECTOR, "span[dir='auto']").text
                    status += 1
                    if driver.find_element(By.CSS_SELECTOR, "span[dir='auto']"):
                        break
                except:
                    status += 1

            about_section = driver.find_element(By.CSS_SELECTOR, "ul").text
            email = re.search(email_pattern, about_section)
            phone_number = re.search(phone_pattern, about_section)
            if email:
                return email.group()
            if phone_number:
                return phone_number.group()
        except Exception as e:
            print(f"Error scraping {page_url}: {e}")
        finally:
            driver.quit()

    def worker_function(self, website):
        return self.scrape(website)

# scraper = CustomScraper()
# print(scraper.worker_function('https://www.facebook.com/digg'))
