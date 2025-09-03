import os
import argparse
import pandas as pd
from dotenv import load_dotenv

from src.selenium_to_sheets.sheets import connect_gsheets, push_to_google_sheet
from src.selenium_to_sheets.scrapers.quotes import scrape_quotes

SCRAPERS = {
    "quotes": scrape_quotes,
}

def main():
    # .env is optional; if it's not present, nothing breaks.
    load_dotenv()

    parser = argparse.ArgumentParser(description="Selenium → Google Sheets")
    sub = parser.add_subparsers(dest="command", required=True)

    s_scrape = sub.add_parser("scrape", help="Run a scraper and upload to Google Sheets")
    s_scrape.add_argument("scraper", choices=SCRAPERS.keys(), help="Which scraper to run")
    s_scrape.add_argument("--pages", type=int, default=10, help="Max pages (if applicable)")

    # New: flags to avoid any environment variables
    s_scrape.add_argument("--sa", dest="sa_path", default=None, help="Path to Service Account JSON")
    s_scrape.add_argument("--sheet", dest="spreadsheet_title", default=None, help="Spreadsheet title to open/create")
    s_scrape.add_argument("--tab", dest="worksheet_title", default=None, help="Worksheet/tab title to create/replace")

    args = parser.parse_args()

    if args.command == "scrape":
        scraper_fn = SCRAPERS[args.scraper]
        df: pd.DataFrame = scraper_fn(max_pages=args.pages)
        print(f"Scraped {len(df)} rows")

        # Prefer CLI flags; fall back to env; then safe defaults
        sa_path = args.sa_path or os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or "./sa_key.json"
        spreadsheet_title = args.spreadsheet_title or os.getenv("SPREADSHEET_TITLE") or "Selenium Scrape Demo"
        worksheet_title = args.worksheet_title or os.getenv("WORKSHEET_TITLE") or args.scraper

        gc = connect_gsheets(sa_path)
        url = push_to_google_sheet(
            client=gc,
            spreadsheet_title=spreadsheet_title,
            worksheet_title=worksheet_title,
            df=df,
            replace_sheet=True,
        )
        print(f"Data written to: {url}")

if __name__ == "__main__":
    main()
