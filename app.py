import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import ta

st.set_page_config(page_title="Indian Stock Dashboard", layout="wide")

st.title("📈 Indian Stock Dashboard")

stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS']

selected_stock = st.selectbox("Select a stock", stocks)
period = st.selectbox("Select time period", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.selectbox("Select data interval", ["1d", "1h", "15m"])

df = yf.download(selected_stock, period=period, interval=interval)
df.dropna(inplace=True)

df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
df['MACD'] = ta.trend.macd_diff(df['Close'])

fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df.index, open=df['Open'], high=df['High'],
    low=df['Low'], close=df['Close'], name='Price'))
fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name="SMA 20"))
fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name="SMA 50"))
fig.update_layout(title=f"{selected_stock} Stock Price with SMA", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Technical Indicators")
st.line_chart(df[['RSI', 'MACD']])

st.subheader("📄 Latest 5 Days")
st.dataframe(df.tail())

csv = df.to_csv().encode('utf-8')
st.download_button("Download CSV", csv, f"{selected_stock}_data.csv", "text/csv")
