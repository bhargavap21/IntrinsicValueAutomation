import time
import yfinance as yf
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define Google Sheets scope and placeholder for your Spreadsheet ID and input range
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "your_spreadsheet_id_here"  # Replace with your spreadsheet ID
RANGE_NAME = "Sheet1!B1"  # Input Ticker

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("path_to_your_credentials.json", SCOPES)  # Replace with your path
            credentials = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        # Read the ticker from the Google Sheet
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        inputTicker = result.get('values', [[None]])[0][0]  # Safely extracting the ticker value

        if not inputTicker:
            print("Ticker not found in the spreadsheet.")
            return

        # Get financial data for the ticker
        data = get_financial_data(inputTicker)

        # Display the data
        for key, value in data.items():
            print(f"{key}: {value}")

        # Update spreadsheet with financial data
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B3", valueInputOption="USER_ENTERED", body={"values": [[data["Interest Expense (Latest Year)"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B4", valueInputOption="USER_ENTERED", body={"values": [[data["Total Debt (Latest Year)"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B6", valueInputOption="USER_ENTERED", body={"values": [[data["Tax Provision (Latest Year)"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B7", valueInputOption="USER_ENTERED", body={"values": [[data["Pretax Income (Latest Year)"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B9", valueInputOption="USER_ENTERED", body={"values": [[data["Treasury Yield"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B10", valueInputOption="USER_ENTERED", body={"values": [[data["Beta"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!B13", valueInputOption="USER_ENTERED", body={"values": [[data["Market Capitalization"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!C17", valueInputOption="USER_ENTERED", body={"values": [[data["Shares Outstanding"]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!D3", valueInputOption="USER_ENTERED", body={"values": [[data["Last 4 Years of Free Cash Flow"][3]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!D4", valueInputOption="USER_ENTERED", body={"values": [[data["Last 4 Years of Free Cash Flow"][2]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!D5", valueInputOption="USER_ENTERED", body={"values": [[data["Last 4 Years of Free Cash Flow"][1]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!D6", valueInputOption="USER_ENTERED", body={"values": [[data["Last 4 Years of Free Cash Flow"][0]]]}).execute()
        sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!C20", valueInputOption="USER_ENTERED", body={"values": [[data["Current Price"]]]}).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")

def get_financial_data(ticker):
    # Download data from Yahoo Finance
    stock = yf.Ticker(ticker)

    # Extracting the requested data
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    info = stock.info

    # Extracting specific data points for the latest year
    interest_expense = financials.loc['Interest Expense'].iloc[0] if 'Interest Expense' in financials.index else None
    total_debt = balance_sheet.loc['Total Debt'].iloc[0] if 'Total Debt' in balance_sheet.index else None
    tax_provision = financials.loc['Tax Provision'].iloc[0] if 'Tax Provision' in financials.index else None
    pretax_income = financials.loc['Pretax Income'].iloc[0] if 'Pretax Income' in financials.index else None
    beta = info.get('beta', None)
    market_cap = info.get('marketCap', None)
    shares_outstanding = info.get('sharesOutstanding', None)
    current_price = info.get('open', None)

    # Free cash flow for the last 4 years
    free_cash_flow = cash_flow.loc['Free Cash Flow'].head(4).tolist() if 'Free Cash Flow' in cash_flow.index else None

    # Web Scrape the treasury yield
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed
    driver.get(f"https://finance.yahoo.com/quote/%5ETNX/")  # Use the correct ticker

    time.sleep(5)  # You can use WebDriverWait for a more robust solution

    # Use XPath to extract the Treasury Yield
    try:
        treasury_yield = driver.find_element(By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/fin-streamer[1]').text
        treasury_yield = float(treasury_yield)/100
    except:
        treasury_yield = None  # Handle the case where the treasury yield is not found
        print("Unable to find Treasury Yield")

    driver.quit()  # Close the browser after the task is complete

    # Formatting and returning the data
    data = {
        "Interest Expense (Latest Year)": interest_expense,
        "Total Debt (Latest Year)": total_debt,
        "Tax Provision (Latest Year)": tax_provision,
        "Pretax Income (Latest Year)": pretax_income,
        "Treasury Yield": treasury_yield,
        "Beta": beta,
        "Market Capitalization": market_cap,
        "Shares Outstanding": shares_outstanding,
        "Last 4 Years of Free Cash Flow": free_cash_flow,
        "Current Price": current_price  # Add current price to data dictionary
    }

    return data

if __name__ == '__main__':
    main()
