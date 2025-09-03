import time
import pandas as pd
from typing import List, Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..driver import get_driver

def _wait_for(driver, by, selector: str, timeout: int = 15):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))

def scrape_quotes(max_pages: int = 5) -> pd.DataFrame:
    driver = get_driver(headless=True)
    records: List[Dict] = []

    try:
        base = "https://quotes.toscrape.com/page/{}/"

        for page in range(1, max_pages + 1):
            url = base.format(page)
            driver.get(url)

            try:
                _wait_for(driver, By.CSS_SELECTOR, ".quote")
            except Exception:
                break

            for card in driver.find_elements(By.CSS_SELECTOR, ".quote"):
                text = card.find_element(By.CSS_SELECTOR, ".text").text.strip()
                author = card.find_element(By.CSS_SELECTOR, ".author").text.strip()
                tags = ", ".join([t.text.strip() for t in card.find_elements(By.CSS_SELECTOR, ".tags .tag")])

                records.append({
                    "quote": text,
                    "author": author,
                    "tags": tags,
                    "source_url": url,
                })

            time.sleep(1.0)

    finally:
        driver.quit()

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.drop_duplicates().reset_index(drop=True)
    return df
