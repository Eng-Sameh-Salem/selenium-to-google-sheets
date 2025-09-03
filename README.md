# Selenium → Google Sheets (Python)

This project demonstrates a clean, reusable workflow to scrape any website using **Selenium**, transform data with **pandas**, and publish the results to **Google Sheets**.

- ✅ Production-ready structure & Dockerfile
- ✅ Works locally or in CI/CD
- ✅ Service Account auth for Google Sheets
- ✅ Easy to adapt: swap the scraper module & CSS selectors

> Demo site: https://quotes.toscrape.com (public, ToS-friendly sandbox).

---

### Requirements
- Python 3.9+ installed and on PATH
- Google Chrome or Chromium installed
- A Google Cloud **Service Account** JSON key file
- Internet access (webdriver-manager will download a matching ChromeDriver)

### Install dependencies
```
pip install -r requirements.txt
```

### Prepare credentials
- Place your Service Account key file somewhere accessible, e.g. `./sa_key.json` in the project root.
- Share your target Google Sheet with the Service Account email (Editor). If the sheet doesn't exist, the script will create it.

### Run
```
python main.py scrape quotes --pages 10 --sa ./sa_key.json --sheet "Selenium Scrape Demo" --tab quotes
```
Explanation of flags:
- `--sa` : path to your Service Account JSON (required if you don't set env vars)
- `--sheet` : Spreadsheet title to open/create
- `--tab` : Worksheet/tab title to create/replace

> The scraper runs in **headless** mode by default. To adapt to another site, create a new module under `src/selenium_to_sheets/scrapers/` using `quotes.py` as a template and register it in `main.py`.
