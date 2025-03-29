import yfinance as yf
import matplotlib.pyplot as plt

ticker = 'NVDA'
stock = yf.Ticker(f"{ticker}")

current_price = stock.history(period="1d")['Close'][-1]
print(f"Current price of {ticker}: ${current_price:.2f}")

data = stock.history(period="6mo")
print(data.tail())

plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label=f"{ticker} Price", color='blue')
plt.title(f"{ticker} Stock Price Over Last 6 Months")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()