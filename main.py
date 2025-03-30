from GUI import TradingApp
import ttkbootstrap as tb

root = tb.Window(themename="darkly")
app = TradingApp(root)

root.mainloop()