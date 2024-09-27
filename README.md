# IntrinsicValueAutomation

A powerful tool that automates real-time financial data collection and analysis on Google Sheets.

**IntrinsicValueAutomation** is a Python tool that automates financial data retrieval from Yahoo Finance and web scraping Treasury Yield data using Selenium. It calculates and updates stock metrics, including intrinsic value data, directly into Google Sheets.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

Install the package via pip:

```sh
pip install intrinsicvalueautomation
```

## Features

* **Automates Financial Data**: Retrieve real-time stock data like Interest Expense, Total Debt, Pretax Income, Free Cash Flow, and more.
* **Web Scraping Integration**: Uses Selenium to scrape Treasury Yield data.
* **Google Sheets Integration**: Updates retrieved financial data directly into a Google Sheets spreadsheet.
* **Dynamic Stock Tickers**: Supports reading stock tickers dynamically from a Google Sheet.

## Google Cloud & API Setup

To run IntrinsicValueAutomation, you'll need to set up a Google Cloud project, enable the Google Sheets API, and configure OAuth credentials. Follow these steps:

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the **Select a project** dropdown at the top of the page, then click **New Project**.
3. Enter your project name and click **Create**.
4. After your project is created, click on the project name to open the dashboard.

### 2. Enable Google Sheets API

1. In the Google Cloud Console, navigate to the **APIs & Services > Library**.
2. Search for **Google Sheets API**.
3. Click **Google Sheets API**, then click **Enable**.

### 3. Set Up OAuth 2.0 Credentials

1. In the Google Cloud Console, go to **APIs & Services > Credentials**.
2. Click **Create Credentials**, then select **OAuth 2.0 Client IDs**.
3. If you haven't set up the OAuth consent screen yet:
   * Click **Configure consent screen**.
   * Select **External** user type and click **Create**.
   * Enter your app details (e.g., app name, user support email, etc.).
   * Click **Save and Continue** (you don't need to fill in other fields for now).
4. After configuring the consent screen, you'll be able to create OAuth 2.0 credentials:
   * Select **Application type: Desktop app**.
   * Enter a name (e.g., "IntrinsicValueAutomation OAuth") and click **Create**.
5. Download the `credentials.json` file and save it to your project folder (where your Python script is located).

### 4. Install Required Python Libraries

1. In your terminal, navigate to the project directory where your `requirements.txt` is located.
2. Install all the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

### 5. Set Up OAuth for Your Application

1. When you run the Python script for the first time, it will open a browser window prompting you to authorize access to your Google Sheets.
2. Once authorized, a `token.json` file will be created in your project directory. This file stores the user's access and refresh tokens, and it will be used for subsequent API calls.

### 6. Add Your Spreadsheet ID

1. Copy the ID of your Google Sheet from its URL. The ID is the string between `/d/` and `/edit` in your Google Sheet URL.

## Usage Example

1. Clone the repository:

```sh
git clone https://github.com/yourusername/IntrinsicValueAutomation.git
```

2. Install the required dependencies:

```sh
pip install -r requirements.txt
```

3. Set up the Google Sheets API:
   * Create a `credentials.json` file in your project folder with your Google Sheets API credentials.

4. Run the program:

```sh
python intrinsicvalueautomation.py
```

## Spreadsheet Structure and Template

IntrinsicValueAutomation uses a specific Google Sheets structure to organize and display financial data. Here's an overview of the spreadsheet:

### Key Components:
- **Company Ticker**: The stock symbol for the company being analyzed (e.g., AAPL for Apple Inc.)
- **WACC**: Weighted Average Cost of Capital calculation
- **DCF**: Discounted Cash Flow analysis
- **Cash Flow Visualization**: A chart showing historical and projected cash flows

### Access the Template:
You can view and copy our [template Google Sheet here](https://docs.google.com/spreadsheets/d/1Y-_X0Hl2Ij7_FYc2Ai64AbhP002Oz9MfKVfxXjuHo7c/edit?usp=sharing).

### CSV Version:
For those who prefer working with raw data, we've included a [CSV version of the template](./template_spreadsheet.csv) in this repository.

### Usage:
1. Make a copy of the template Google Sheet or download the CSV.
2. Update the 'Company Ticker' cell with your desired stock symbol.
3. Run the IntrinsicValueAutomation script to populate the spreadsheet with real-time data.

Note: The script will automatically update most fields. Manual adjustments may be needed for some projections or assumptions.

## Command-Line Arguments

```sh
python intrinsicvalueautomation.py --help
```

## Example Output

After running, the program fetches stock data from Yahoo Finance and updates your Google Sheet with the following fields:

* **Interest Expense**
* **Total Debt**
* **Pretax Income**
* **Treasury Yield**
* **Free Cash Flow** (Last 4 Years)
* **Market Capitalization**
* **Shares Outstanding**

## Web Scraping Setup

1. Install **Selenium** and the **ChromeDriver** to allow web scraping of Treasury Yield data.

```sh
pip install selenium
```

2. Download and install ChromeDriver and ensure it's added to your system's PATH.

## Sample Request Flow

1. **Fetching Financial Data**: The tool fetches data from Yahoo Finance using the `yfinance` library.
2. **Scraping Treasury Yield**: Selenium scrapes the Treasury Yield from finance websites, and the data is formatted and displayed.
3. **Google Sheets Update**: All fetched data is pushed directly to the linked Google Sheet.

## Sample Selenium Code for Scraping

```python
driver = webdriver.Chrome()
driver.get(f"https://finance.yahoo.com/quote/%5ETNX/")
treasury_yield = driver.find_element(By.XPATH, 'xpath_to_element').text
driver.quit()
```

## Disclaimer

If Selenium or other packages do not work globally on Windows, install the package in a local virtual environment:

```sh
python3 -m venv env
source env/bin/activate
pip install intrinsicvalueautomation
```

## IO Redirection

Save program output for later analysis:

```sh
python intrinsicvalueautomation.py > output.log 2>&1
```

## Development Setup

Clone the repository and install the necessary packages listed in `requirements.txt`:

```sh
pip install -r requirements.txt
```

## Meta

[Bhargava Perumalla] – [bhargavap740@gmail.com]

Distributed under the MIT license. See `LICENSE` for more information.

https://github.com/yourusername/IntrinsicValueAutomation

## Contributing

1. Fork the repository (https://github.com/bhargava21/IntrinsicValueAutomation/fork)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
