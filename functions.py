import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd

def NASDAQ_TO_NAME(nasdaqCode):
    nasdaq_codes = pd.read_csv('Data/nasdaq_screener_1743286582710.csv')
    return nasdaq_codes.loc[nasdaq_codes['Symbol'] == nasdaqCode, 'Name'].values[0]

def generate_stock_graph(ticker, short_period='1d', long_period='6mo'):
    '''A Function that returns a matplotlib graph, used for stock preview tab in this app.
    -> ticker is the NASDAQ code for a stock (Like AAPL; NVDA; AMZN)
    -> amount is the amount of stocks in the input
    -> short_period shows the intervals in which stock prices are shown
    -> long_period shows how much time back is going to be shown'''
    if len(ticker.split(',')) > 1:
        colors = ['blue', 'red', 'green', 'yellow', 'orange']
        seperator = ','

        tickers = ticker.split(seperator)
        tickers = [i.strip() for i in tickers]

        fig, ax = plt.subplots(figsize=(12, 6))
        for ticker in tickers:
            stock = yf.Ticker(f"{ticker}")
            data = stock.history(period=long_period)
            ax.plot(data.index, data['Close'], label=f"{NASDAQ_TO_NAME(ticker)} price", color=colors[tickers.index(ticker)])
        ax.set_title(f"Stock Price(-s) Over Last 6 Months")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        ax.grid(True)

        return fig  # Return the figure object
    else:
        stock = yf.Ticker(f"{ticker}")

        data = stock.history(period=long_period)
        print(data.tail())

        # Create the plot
        fig, ax = plt.subplots(figsize=(12, 6))  # Create a figure and axes explicitly
        ax.plot(data.index, data['Close'], label=f"{NASDAQ_TO_NAME(ticker)} price", color='blue')
        ax.set_title(f"{NASDAQ_TO_NAME(ticker)} Stock Price Over Last 6 Months")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        ax.grid(True)

        return fig  # Return the figure object