import pandas as pd
import numpy as np
import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H-%M-%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format) 
    with open("./code_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')


def extract(url, table_attribs):
    page = requests.get(url).text
    data = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    
    for row in rows:
        col = row.find_all('td')
        
        if len(col) > 2 and len(col[0].find_all('a')) > 0:
            Bank_Name = col[0].find_all('a')[1].get('title', col[0].text).strip()
            
            if col[2].contents and col[2].contents[0].strip() != '':
                Market_Cap = float(col[2].contents[0][:-1])
            else:
                Market_Cap = np.nan
                
            data_dict = {"Bank_Name": Bank_Name, "Market_Cap": Market_Cap}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df, df1], ignore_index=True)
    return df

def transform(df):

    exchange_rates_df = pd.read_csv('exchange_rate.csv')
    exchange_rate = exchange_rates_df.set_index('Currency').to_dict()['Rate']
    MC_USD_Billion = df["Market_Cap"].tolist()
    MC_EUR_Billion = [np.round(x*exchange_rate['EUR'],2) for x in MC_USD_Billion]
    MC_GBP_Billion = [np.round(x*exchange_rate['GBP'],2) for x in MC_USD_Billion]
    MC_INR_Billion = [np.round(x*exchange_rate['INR'],2) for x in MC_USD_Billion]
    df["MC_EUR_Billion"] = MC_EUR_Billion
    df["MC_GBP_Billion"] = MC_GBP_Billion
    df["MC_INR_Billion"] = MC_INR_Billion
    df=df.rename(columns = {
        "MC_EUR_Billion":"MC_EUR_Billion",
        "MC_GBP_Billion":"MC_GBP_Billion",
        "MC_INR_Billion":"MC_INR_Billion"})
    return df

def load_to_csv(df, csv_path):
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)


def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)


url = "https://en.wikipedia.org/wiki/List_of_largest_banks"
table_attribs = ["Bank_Name", "Market_Cap"]
db_name = 'Banks.db'
table_name = 'Largest_banks'
csv_path = './Largest_banks_data.csv'

log_progress('Preliminaries complete. Initiating ETL process')

df = extract(url, table_attribs)
#print(df)
log_progress('Data extraction complete. Initiating Transformation process')

df = transform(df)
#print(df)
log_progress('Data transformation complete. Initiating loading process')

load_to_csv(df, csv_path)
log_progress('Data saved to CSV file')

sql_connection = sqlite3.connect('Banks.db')
log_progress('SQL Connection initiated.')

load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query')

query_statements = [
    f"SELECT * FROM {table_name}",
    "SELECT AVG(MC_GBP_Billion) FROM Largest_banks",
    "SELECT Bank_Name from Largest_banks LIMIT 5"
]
for query_statement in query_statements:
    run_query(query_statement, sql_connection)

log_progress('Process Complete.')

sql_connection.close()

#url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
