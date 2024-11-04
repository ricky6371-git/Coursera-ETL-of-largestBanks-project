# Coursera-ETL-of-largestBanks-project
# ETL Process for Largest Banks Data

This project extracts data on the largest banks from Wikipedia, transforms the data to include market capitalization in various currencies, and loads it into a SQLite database and CSV file. It also provides queries to interact with the stored data.

## Table of Contents

- [Getting Started](#getting-started)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [ETL Process](#etl-process)
  - [1. Extract](#1-extract)
  - [2. Transform](#2-transform)
  - [3. Load](#3-load)
- [Usage](#usage)
- [Logging](#logging)
- [Sample Queries](#sample-queries)

## Getting Started

### Requirements

This project requires:
- Python 3.7+
- The following Python libraries:
  - `pandas`
  - `numpy`
  - `requests`
  - `BeautifulSoup4`
  - `sqlite3`
  - `datetime`

Install the required packages via pip:
```bash
pip install pandas numpy requests beautifulsoup4
```

### Project Structure

```plaintext
.
├── main_script.py         # Main Python script for ETL
├── exchange_rate.csv      # CSV with exchange rates for conversion
├── code_log.txt           # Log file for tracking progress
├── Largest_banks_data.csv # Output CSV with processed data
└── README.md              # Project documentation
```

## ETL Process

The ETL (Extract, Transform, Load) process follows these steps:

### 1. Extract

The script fetches bank data from Wikipedia, extracting the name and market cap from the page and stores it in a DataFrame.

### 2. Transform

The transformation stage:
- Converts USD market cap to EUR, GBP, and INR using rates from `exchange_rate.csv`.
- Adds these converted columns to the DataFrame.

### 3. Load

The data is saved to:
- A CSV file (`Largest_banks_data.csv`).
- A SQLite database table (`Largest_banks`).

## Usage

Run the ETL script:
```bash
python main_script.py
```

Ensure `exchange_rate.csv` is in the same directory with the currency exchange rates formatted as follows:

| Currency | Rate |
|----------|------|
| EUR      | 0.85 |
| GBP      | 0.76 |
| INR      | 74.50|

### Logging

The script logs each stage's progress to `code_log.txt` with timestamps.

### Sample Queries

The script runs SQL queries on the loaded database, such as:
- `SELECT * FROM Largest_banks` - Shows all records.
- `SELECT AVG(MC_GBP_Billion) FROM Largest_banks` - Gets average market cap in GBP.
- `SELECT Bank_Name FROM Largest_banks LIMIT 5` - Lists the first 5 banks.

You can modify or add queries in the `query_statements` list in the script.

## License

This project is open-source. Feel free to modify and adapt it.
```

This README covers all important sections, making it easy for others to understand the setup, dependencies, and usage of your ETL project. Let me know if you'd like to add more details!
