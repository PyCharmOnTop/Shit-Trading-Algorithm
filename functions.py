import yfinance as yf
import matplotlib.pyplot as plt

def generate_stock_graph(ticker, short_period='1d', long_period='6mo'):
    '''A Function that returns a matplotlib graph, used for stock preview tab in this app.
    -> ticker is the NASDAQ code for a stock (Like AAPL; NVDA; AMZN)
    -> short_period shows the intervals in which stock prices are shown
    -> long_period shows how much time back is going to be shown'''
    stock = yf.Ticker(f"{ticker}")

    current_price = stock.history(period=short_period)['Close'][-1]
    print(f"Current price of {ticker}: ${current_price:.2f}")

    data = stock.history(period=long_period)
    print(data.tail())

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))  # Create a figure and axes explicitly
    ax.plot(data.index, data['Close'], label=f"{ticker} Price", color='blue')
    ax.set_title(f"{ticker} Stock Price Over Last 6 Months")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    ax.grid(True)

    return fig  # Return the figure object