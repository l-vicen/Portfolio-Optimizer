from gsheetsdb import connect
import gspread
import streamlit as st
import datetime


# Empty google sheet for tickers when list_of_stocks changes
def change():
    sa = gspread.service_account("credentials.json")
    sh = sa.open("Portfolio")
    sh.values_clear("Sheet1!A2:A10000")


# Get previous selected portfolio
def load_tickers():
    conn = connect()

    @st.cache(ttl=600)
    def run_query(query):
        rows = conn.execute(query, headers=1)
        return rows

    sheet_url = st.secrets["tickers_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    tickers = []
    for row in rows:
        tickers.append(f"{row.ticker}")

    return tickers


# Save current portfolio
def save_tickers(list_of_stocks):
    sa = gspread.service_account("credentials.json")
    sh = sa.open("Portfolio")
    worksheet = sh.get_worksheet(0)

    i = 0
    for j in range(2, len(list_of_stocks) + 2):
        worksheet.update_cell(j, 1, list_of_stocks[i])
        i += 1


# Save expected performance
def save_expected_performance(expected_performance, tickers, method):
    sa = gspread.service_account("credentials.json")
    sh = sa.open("Portfolio")
    worksheet = sh.get_worksheet(1)

    l = len(worksheet.col_values(1))+1

    worksheet.update_cell(l, 1, method)
    worksheet.update_cell(l, 2, str(tickers))
    worksheet.update_cell(l, 3, expected_performance[0])
    worksheet.update_cell(l, 4, expected_performance[1])
    worksheet.update_cell(l, 5, expected_performance[2])
    worksheet.update_cell(l, 6, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
