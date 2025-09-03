import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def connect_gsheets(service_account_json_path: str) -> gspread.Client:
    creds = Credentials.from_service_account_file(service_account_json_path, scopes=SCOPES)
    return gspread.authorize(creds)

def push_to_google_sheet(client: gspread.Client, spreadsheet_title: str, worksheet_title: str, df: pd.DataFrame, replace_sheet: bool = True) -> str:
    try:
        sh = client.open(spreadsheet_title)
    except gspread.SpreadsheetNotFound:
        sh = client.create(spreadsheet_title)

    try:
        ws = sh.worksheet(worksheet_title)
        if replace_sheet:
            sh.del_worksheet(ws)
            ws = sh.add_worksheet(title=worksheet_title, rows="100", cols="26")
        else:
            ws.clear()
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_title, rows="100", cols="26")

    if df.empty:
        ws.update([["No data"]])
    else:
        values = [df.columns.tolist()] + df.astype(str).values.tolist()
        ws.update(values)

    return sh.url
