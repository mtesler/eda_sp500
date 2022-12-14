import base64
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
selected_sector = []


def clear_multi():
    st.session_state.multiselect = sorted_sector_unique
    return


multi = st.sidebar.multiselect(
    'Sector', sorted_sector_unique, default=sorted_sector_unique, key='multiselect')

st.sidebar.button('Select all sectors', on_click=clear_multi)

# Sidebar - Number of companies selection (to show on charts)
num_company = st.sidebar.slider('Number of Companies', 1, 5)

# Filtering data
df_selected_sector = df[(df['GICS Sector'].isin(multi))]

st.header('Display companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(
    df_selected_sector.shape[1]) + ' columns.')
st.write(df_selected_sector)

# Download S&P500 data


def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href


st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)

# Download financial data
data = yf.download(tickers=list(df_selected_sector[:10].Symbol), period='ytd', interval='1d',
                   group_by='ticker', auto_adjust=True, prepost=True, threads=True, proxy=None)

data['Date'] = data.index
data.reset_index(drop=True, inplace=True)

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
    return st.pyplot()


# Show / hide plots button
if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)

st.set_option('deprecation.showPyplotGlobalUse', False)
