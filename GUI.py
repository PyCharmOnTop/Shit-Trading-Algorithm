import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
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
        self.root = root # Makes the root variable equal to the root argument
        self.root.title("Trading Algorithm App") # Sets the app title
        self.root.geometry("1400x800")  # Increased size for better zoom

        # Theme Setup
        self.style = tb.Style() # Makes a style variable
        self.theme_var = tk.StringVar(value=self.style.theme_use())
        self.style.theme_use("darkly") # Sets the default theme

        # Main layout frames
        self.main_frame = ttk.Frame(root) # Adds the main frame
        self.main_frame.pack(fill=tk.BOTH, expand=True) # Packs the main frame

        self.side_panel = ttk.Frame(self.main_frame, width=250, padding=20, relief="ridge") # Makes the side panel frame
        self.side_panel.pack(side=tk.LEFT, fill=tk.Y) # Packs the side panel frame

        self.notebook = ttk.Frame(self.main_frame) # Adds a notebook frame
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20) # Packs the notebook frame

        # Tabs
        self.tab1 = ttk.Frame(self.notebook) # Creates the first tab
        self.create_algorithm_settings()

        self.tab2 = ttk.Frame(self.notebook) # Creates the second tab
        self.create_stock_preview()

        self.tab3 = ttk.Frame(self.notebook) # Creates the third tab
        self.create_trading_helper()

        self.tab4 = ttk.Frame(self.notebook) # Creates the fourth tab
        self.create_future_predictions()

        self.settings_tab = ttk.Frame(self.notebook) # Creates the settings tab
        self.create_settings()

        self.create_side_menu() # Creates the side menu and displays the main menu
        self.show_tab(self.tab1)

    def create_side_menu(self):
        buttons = [
            ("⚙ Algorithm Settings", self.tab1),
            ("📈 Stock Preview", self.tab2),
            ("💰 Trading Helper", self.tab3),
            ("🔮 Future Predictions", self.tab4),
            ("⚙ Settings", self.settings_tab)
        ] # Is a list of tuples which store a buttons name and which tab it goes to

        for text, tab in buttons:
            btn = ttk.Button(self.side_panel, text=text, command=lambda t=tab: self.show_tab(t),
                             style="primary.Outline.TButton") # Creates a button for every tab
            btn.pack(fill=tk.X, pady=12, ipady=8)

    def show_tab(self, tab):
        for child in self.notebook.winfo_children():
            child.pack_forget()
        tab.pack(fill=tk.BOTH, expand=True) # Unpacks the previous tab and packs the new one to display it


    # Create the tabs
    # Creates the algorithm settings tab
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

    # Creates the stock preview tab
    def create_stock_preview(self):
        frame = ttk.Frame(self.tab2, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Enter NASDAQ Code:", font=("Arial", 16, "bold")).pack(pady=10)
        self.stock_input = ttk.Entry(frame, font=("Arial", 14))
        self.stock_input.pack(pady=10, ipadx=10, ipady=8)
        self.stock_input.bind("<Return>", self.validate_stock)


        self.stock_chart_frame = ttk.Frame(frame, borderwidth=4, relief="groove")
        self.stock_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    # Creates the future predictions preview tab
    def create_future_predictions(self):
        frame = ttk.Frame(self.tab4, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="COMING SOON!", font=("Arial", 48, "bold")).pack(pady=10)

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
        try:
            self.draw_chart(self.stock_chart_frame, lambda: generate_stock_graph(stock_code))
        except AttributeError:
            print('Invalid')

    # Creates the trading helper tab
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

    # Creates the settings tab
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

