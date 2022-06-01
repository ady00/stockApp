import yfinance as yf
import streamlit as st 
import pandas as pd
import plotly.graph_objects as go
import requests


st.write("""
# Simple Stock Price App
""")




tickerSymbol = st.text_input('Enter Stock Symbol', 'QQQ')

st.write(tickerSymbol, "stock information")



tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2021-12-30')


st.write("""
## Closing Price
""")

st.line_chart(tickerDf.Close)
st.write("""
## Volume Price
""")
st.line_chart(tickerDf.Volume)
st.write("""
## Opening Price
""")
st.line_chart(tickerDf.Open)


st.write("""
## High
""")
st.line_chart(tickerDf.High)

st.write("""
## Low
""")
st.line_chart(tickerDf.Low)

st.write("""
## Dividends
""")
st.line_chart(tickerDf.Dividends)


API_URL = "https://www.alphavantage.co/query"

data = { "function": "TIME_SERIES_DAILY",
    "symbol": tickerSymbol,
    "outputsize" : "compact",
    "datatype": "json",
    "apikey": "XUU9EQK9LZIWWZGG" } 


response = requests.get(API_URL, data).json()

data = pd.DataFrame.from_dict(response['Time Series (Daily)'], orient= 'index').sort_index(axis=1)
data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
data['Date'] = data.index

fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name=tickerSymbol)])

fig.update_layout(
    title=tickerSymbol+ ' Daily Chart',
    xaxis_title="Date",
    yaxis_title="Price ($)",
    font=dict(
        family="Courier New, monospace",
        size=12,
        color="white"
    )
)

st.plotly_chart(fig,  use_container_width=True)



st.write("# Company Info")
st.write(tickerData.info)
st.write(tickerData.calendar)
st.write(tickerData.recommendations)


st.write("Advay B")


