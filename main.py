from GUI import TradingApp
import ttkbootstrap as tb
import functions

print(functions.NASDAQ_TO_NAME('AAPL'))

root = tb.Window(themename="darkly")
app = TradingApp(root)
root.mainloop()