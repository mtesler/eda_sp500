import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.title('S&P500 App')

st.markdown("""
This app retrieves the list of the **S&P500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P500 data


@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header=0)
    df = html[0]
    return df


df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique)

# Download financial data
data = yf.download(tickers=list(df.Symbol), period='ytd', interval='1d',
                   group_by='ticker', auto_adjust=True, prepost=True, threads=True, proxy=None)


data['Date'] = data.index
data.reset_index(drop=True, inplace=True)
st.write(df)

# Create plot based on closing price


def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing price', fontweight='bold')
    return plt.show()


price_plot('AAPL')
