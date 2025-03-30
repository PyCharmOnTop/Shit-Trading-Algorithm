import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import time
import datetime
import numpy as np
from plyer import notification  # For desktop notifications


class MomentumAlgorithm:
    def __init__(self, ticker, interval='1m', rsi_window=14, atr_window=14):
        self.ticker = ticker
        self.interval = interval
        self.rsi_window = rsi_window
        self.atr_window = atr_window
        self.data = None
        self.risk_level = -1
        self.current_price = -1

        if not ticker:
            raise ValueError("Stock symbol cannot be empty")

    def fetch_live_data(self):
        try:
            print(f"Fetching data for: {self.ticker}...")

            stock_data = yf.download(self.ticker, period="1d", interval="1m")

            if stock_data.empty:
                print("Error: No data received from yfinance.")
                return -1  # Return error code

            # Store fetched data
            self.data = stock_data

            # Ensure indicators are calculated before accessing RSI
            self.calculate_indicators()

            # Extract latest close price
            self.current_price = float(stock_data["Close"].dropna().iloc[0])

            print(f"Fetched Price: {self.current_price}")
            print(self.data.head())
            return self.current_price

        except Exception as e:
            print(f"Error in fetch_live_data: {e}")
            return -1

    def calculate_indicators(self):
        """Calculate RSI, ATR, and MACD for buy/sell signals and risk assessment."""
        delta = self.data['Close'].diff()

        gain = np.where(delta > 0, delta, 0).flatten()
        loss = np.where(delta < 0, -delta, 0).flatten()

        avg_gain = pd.Series(gain, index=self.data.index).rolling(window=self.rsi_window).mean()
        avg_loss = pd.Series(loss, index=self.data.index).rolling(window=self.rsi_window).mean()

        rs = avg_gain / avg_loss
        self.data['RSI'] = 100 - (100 / (1 + rs))

        # Calculate ATR
        high = self.data['High']
        low = self.data['Low']
        close = self.data['Close']
        tr = pd.concat([high - low, abs(high - close.shift(1)), abs(low - close.shift(1))], axis=1).max(axis=1)
        self.data['ATR'] = tr.rolling(window=self.atr_window).mean()

        # Calculate MACD
        self.calculate_macd()

        # Update risk level
        self.risk_level = self.data['ATR'].iloc[-1]

    def check_signals(self):
        """Check buy and sell signals using RSI and MACD crossover."""
        if len(self.data) < 2:
            return None

        latest_rsi = self.data['RSI'].iloc[-1]
        previous_rsi = self.data['RSI'].iloc[-2]
        latest_macd = self.data['MACD'].iloc[-1]
        latest_macd_signal = self.data['MACD_signal'].iloc[-1]

        # Buy Signal: RSI < 30 + MACD crosses above Signal Line
        if latest_rsi < 30 and previous_rsi >= 30 and latest_macd > latest_macd_signal:
            self.send_notification("Buy Signal", f"Buy {self.ticker} at {self.data['Close'].iloc[-1]}")
            return "BUY"

        # Sell Signal: RSI > 70 + MACD crosses below Signal Line
        elif latest_rsi > 70 and previous_rsi <= 70 and latest_macd < latest_macd_signal:
            return "SELL"

        return None

    def send_notification(self, title, message):
        """Send desktop notification."""
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )

    def calculate_macd(self, fast=12, slow=26, signal=9):
        """Calculate MACD and Signal Line."""
        self.data['EMA_fast'] = self.data['Close'].ewm(span=fast, adjust=False).mean()
        self.data['EMA_slow'] = self.data['Close'].ewm(span=slow, adjust=False).mean()
        self.data['MACD'] = self.data['EMA_fast'] - self.data['EMA_slow']
        self.data['MACD_signal'] = self.data['MACD'].ewm(span=signal, adjust=False).mean()

    def update_chart(self):
        """Update the stock price chart efficiently without memory leaks."""
        self.fetch_live_data()
        plt.ion()

        # Create a single figure and reuse it
        fig, ax = plt.subplots(figsize=(10, 5))

        try:
            while plt.fignum_exists(fig.number):
                self.fetch_live_data()
                if self.data is None or self.data.empty:
                    continue

                ax.clear()  # Clears the previous plot instead of making a new figure
                ax.plot(self.data.index, self.data['Close'], label='Stock Price', color='blue')

                signal = self.check_signals()
                if signal == "BUY":
                    ax.scatter(self.data.index[-1], self.data['Close'].iloc[-1], color='green', label='Buy Signal',
                               zorder=5)
                elif signal == "SELL":
                    ax.scatter(self.data.index[-1], self.data['Close'].iloc[-1], color='red', label='Sell Signal',
                               zorder=5)

                ax.set_title(f"{self.ticker} Stock Price")
                ax.set_xlabel("Time")
                ax.set_ylabel("Price")
                ax.legend()
                plt.draw()
                plt.pause(1)

        except Exception as e:
            print(f"Error in update_chart: {e}")

        finally:
            plt.close(fig)  # Closes the figure properly to free up memory


    def get_current_price(self):
        if self.data is not None and not self.data.empty:
            return float(self.data['Close'].iloc[0])  # Ensure float return
        return -1  # Return -1 if no data is available


if __name__ == "__main__":
    trader = MomentumAlgorithm("NVDA")
    trader.update_chart()