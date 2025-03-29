import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from functions import generate_stock_graph

# Sample NASDAQ validation list
NASDAQ_VALID = list(pd.read_csv('Data/nasdaq_screener_1743286582710.csv')['Symbol'])

class TradingApp:
    """
    A trading algorithm GUI application.

    Methods:
    - buy_signal(): Displays a BUY signal.
    - sell_signal(): Displays a SELL signal.
    - draw_chart(frame, plot_function): Draws a stock chart using an external function.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Algorithm App")
        self.root.geometry("1400x800")  # Increased size for better zoom

        # Theme Setup
        self.style = tb.Style()
        self.theme_var = tk.StringVar(value=self.style.theme_use())
        self.style.theme_use("darkly")

        # Main layout frames
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.side_panel = ttk.Frame(self.main_frame, width=250, padding=20, relief="ridge")
        self.side_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.notebook = ttk.Frame(self.main_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.create_algorithm_settings()

        self.tab2 = ttk.Frame(self.notebook)
        self.create_stock_preview()

        self.tab3 = ttk.Frame(self.notebook)
        self.create_trading_helper()

        self.settings_tab = ttk.Frame(self.notebook)
        self.create_settings()

        self.create_side_menu()
        self.show_tab(self.tab1)

    def create_side_menu(self):
        buttons = [
            ("⚙ Algorithm Settings", self.tab1),
            ("📈 Stock Preview", self.tab2),
            ("💰 Trading Helper", self.tab3),
            ("⚙ Settings", self.settings_tab)
        ]

        for text, tab in buttons:
            btn = ttk.Button(self.side_panel, text=text, command=lambda t=tab: self.show_tab(t),
                             style="primary.Outline.TButton")
            btn.pack(fill=tk.X, pady=12, ipady=8)

    def show_tab(self, tab):
        for child in self.notebook.winfo_children():
            child.pack_forget()
        tab.pack(fill=tk.BOTH, expand=True)

    def create_algorithm_settings(self):
        frame = ttk.Frame(self.tab1, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Algorithm Choice:", font=("Arial", 16, "bold")).pack(pady=10)
        self.algo_choice = ttk.Combobox(frame, values=["Algo1", "Algo2", "Algo3"], state="readonly", font=("Arial", 14))
        self.algo_choice.pack(pady=10, ipadx=10, ipady=8)

        ttk.Label(frame, text="Time Interval (Seconds):", font=("Arial", 16, "bold")).pack(pady=10)
        self.time_interval = ttk.Scale(frame, from_=1, to=60, orient='horizontal', length=400)
        self.time_interval.pack(pady=10)

        for label_text in ["Min Stock Price:", "Max Stock Price:"]:
            ttk.Label(frame, text=label_text, font=("Arial", 16, "bold")).pack(pady=10)
            ttk.Entry(frame, font=("Arial", 14)).pack(pady=10, ipadx=10, ipady=8)

    def create_stock_preview(self):
        frame = ttk.Frame(self.tab2, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Enter NASDAQ Code:", font=("Arial", 16, "bold")).pack(pady=10)
        self.stock_input = ttk.Entry(frame, font=("Arial", 14))
        self.stock_input.pack(pady=10, ipadx=10, ipady=8)
        self.stock_input.bind("<Return>", self.validate_stock)

        self.stock_chart_frame = ttk.Frame(frame, borderwidth=4, relief="groove")
        self.stock_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def draw_chart(self, frame, plot_function):
        """
        Draws a stock chart using an external function.

        Parameters:
        - frame: The frame where the chart will be placed.
        - plot_function: A function that generates a Matplotlib figure.
        """
        for widget in frame.winfo_children():
            widget.destroy()
        fig = plot_function()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def validate_stock(self, event=None):
        stock_code = self.stock_input.get().strip().upper()
        if stock_code in NASDAQ_VALID:
            print(f"Valid stock: {stock_code}")
            self.draw_chart(self.stock_chart_frame, lambda: generate_stock_graph(stock_code))
        else:
            print(f"Invalid stock: {stock_code}")

    def create_trading_helper(self):
        frame = ttk.Frame(self.tab3, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        self.stock_name_label = ttk.Label(frame, text="Stock: None", font=("Arial", 18, "bold"))
        self.stock_name_label.pack(pady=15)

        self.trading_chart_frame = ttk.Frame(frame, borderwidth=4, relief="groove")
        self.trading_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.trade_action_label = ttk.Label(frame, text="", font=("Arial", 32, "bold"))
        self.trade_action_label.pack(pady=25)

    def buy_signal(self):
        self.trade_action_label.config(text="BUY", foreground="green")

    def sell_signal(self):
        self.trade_action_label.config(text="SELL", foreground="red")

    def create_settings(self):
        frame = ttk.Frame(self.settings_tab, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Volume:", font=("Arial", 16, "bold")).pack(pady=10)
        self.volume = ttk.Scale(frame, from_=0, to=100, orient='horizontal', length=400)
        self.volume.pack(pady=10)

        ttk.Label(frame, text="Theme:", font=("Arial", 16, "bold")).pack(pady=10)
        theme_dropdown = ttk.Combobox(frame, values=self.style.theme_names(), state="readonly",
                                      textvariable=self.theme_var, font=("Arial", 14))
        theme_dropdown.pack(pady=10, ipadx=10, ipady=8)
        theme_dropdown.bind("<<ComboboxSelected>>", self.change_theme)

    def change_theme(self, event):
        self.style.theme_use(self.theme_var.get())

