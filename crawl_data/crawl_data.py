# import build-in dependencies
from typing import *

# import 3rd part dependencies
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import project dependencies
from core.config import config


def get_driver():
    driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()

    prefs = {
        'download.default_directory': config.raw_data_dir,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    }

    options.add_experimental_option('prefs', prefs)
    options.add_argument('--start-maximized')
    options.add_argument("--headless")
    driver = webdriver.Chrome(options)

    return driver

def crawl_hrefs(href: str, num_pages = 10):
    driver = get_driver()
    driver.get(config.base_url + href)

    hrefs = []
    for i in tqdm(range(num_pages), desc = "Đang crawl đường dẫn đến các file văn bản..."):
        soup = BeautifulSoup(driver.page_source, "html.parser")

        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.pagination li.next"))
        )

        main_div = soup.find("div", class_ = "table-content")
        main_table = main_div.find("table", class_ = "table-cb")

        for tr in main_table.find_all("tr", class_ = "head"):
            td = tr.find("td")

            if not td: continue

            hrefs.append(config.base_url + f"/{td.find('a')['href']}")
        
        next_button.click()
    
    driver.quit()
    return hrefs

def crawl_pdfs(hrefs):
    num_hrefs = len(hrefs)
    driver = get_driver()

    for i in tqdm(range(num_hrefs), desc = "Đang tải các file văn bản..."):
        href = hrefs[i]
        driver.get(href)

        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.tab-content div[class='tab-pane active'] table.table-info-row td#content-attachments div"))
            )

            download_buttons = driver.find_elements(
                By.CSS_SELECTOR,
                "div.tab-content div[class='tab-pane active'] table.table-info-row td#content-attachments div"
            )

            for download_button in download_buttons:
                download_button.click()

        except:
            continue
    
    driver.quit()

    