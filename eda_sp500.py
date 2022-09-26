import pandas as pd
import streamlit as st
import yfinance as yf


def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()

# Download financial data
data = yf.download(tickers=list(df.Symbol), period='ytd', interval='1d',
                   group_by='ticker', auto_adjust=True, prepost=True, threads=True, proxy=None)


data['Date'] = data.index
data.reset_index(drop=True, inplace=True)
