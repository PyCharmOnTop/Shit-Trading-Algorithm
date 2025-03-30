import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt

from algorithms import MomentumAlgorithm
from functions import generate_stock_graph, NASDAQ_TO_NAME

# Sample NASDAQ validation list
NASDAQ_VALID = list(pd.read_csv('Data/nasdaq_screener_1743286582710.csv')['Symbol'])
global_algo_choice = None

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
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Increased size for better zoom



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
        global global_algo_choice
        frame = ttk.Frame(self.tab1, padding=30)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Algorithm Choice:", font=("Arial", 16, "bold")).pack(pady=10)
        self.algo_choice = ttk.Combobox(frame, values=["Momentum Algorithm", "Coming Soon!", "Coming Soon!"], state="readonly", font=("Arial", 18))
        self.algo_choice.pack(pady=10, ipadx=10, ipady=8)

        ttk.Label(frame, text="Time Interval (Seconds):", font=("Arial", 16, "bold")).pack(pady=10)
        self.time_interval = ttk.Scale(frame, from_=1, to=60, orient='horizontal', length=400)
        self.time_interval.pack(pady=10)

        for label_text in ["Min Stock Price:", "Max Stock Price:"]:
            ttk.Label(frame, text=label_text, font=("Arial", 16, "bold")).pack(pady=10)
            ttk.Entry(frame, font=("Arial", 14)).pack(pady=10, ipadx=10, ipady=8)
        self.algo_choice.bind("<<ComboboxSelected>>", self.set_global_algo)

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
        # Destroy previous widgets to prevent memory leaks
        for widget in frame.winfo_children():
            widget.destroy()

        fig = plot_function()  # Generate the new figure
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Close the figure to release memory
        plt.close(fig)

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

        ttk.Label(frame, text="Enter NASDAQ Code:", font=("Arial", 16, "bold")).pack(pady=10)
        self.stock_input_helper = ttk.Entry(frame, font=("Arial", 14))
        self.stock_input_helper.pack(pady=10, ipadx=10, ipady=8)
        self.stock_input_helper.bind("<Return>", self.start_updating)

        self.stock_name_label = ttk.Label(frame, text="Stock: N/A", font=("Arial", 18, "bold"))
        self.stock_name_label.pack(pady=15)

        self.trading_chart_frame = ttk.Frame(frame, borderwidth=4, relief="groove")
        self.trading_chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.trade_action_label = ttk.Label(frame, text="", font=("Arial", 32, "bold"))
        self.trade_action_label.pack(pady=15)

        self.risk_label = ttk.Label(frame, text="Risk Level: N/A", font=("Arial", 16))
        self.risk_label.pack(pady=10)

        self.current_price_label = ttk.Label(frame, text="Current Price: N/A", font=("Arial", 16, "bold"))
        self.current_price_label.pack(pady=10)

        self.is_updating = False
        self.current_stock = ""

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

    def set_global_algo(self, event):
        global global_algo_choice
        global_algo_choice = self.algo_choice.get()

        # If "Momentum Algorithm" is selected, update Trading Helper
        if global_algo_choice == "Momentum Algorithm":
            self.update_trading_helper()  # Use class's ticker argument

    def start_updating(self, event=None):
        stock_symbol = self.stock_input_helper.get().strip().upper()
        if stock_symbol == self.current_stock:
            return

        self.current_stock = stock_symbol
        self.is_updating = True
        self.update_trading_helper()

    def stop_updating(self, event=None):
        # Stop the updates if the input is changed
        self.is_updating = False
        # Clear any old data or UI updates (optional)
        self.trade_action_label.config(text="")
        self.risk_label.config(text="Risk Level: N/A")
        self.stock_name_label.config(text="Stock: N/A")
        self.stock_input_helper.config(state="normal")

    def update_trading_helper(self):
        if not self.is_updating or not self.current_stock:
            return

        try:
            print(f"Creating MomentumAlgorithm instance for {self.current_stock}")  # Debugging
            algo = MomentumAlgorithm(self.current_stock)  # Ensure the stock symbol is passed correctly
            algo.fetch_live_data()

            self.risk_label.config(text=f"Risk Level: {round((algo.risk_level) * 100)}%")
            self.current_price_label.config(text=f"Current Price: {algo.get_current_price():.2f}")

            signal = algo.check_signals()
            if signal == "BUY":
                self.trade_action_label.config(text="BUY", foreground="green")
            elif signal == "SELL":
                self.trade_action_label.config(text="SELL", foreground="red")
            else:
                self.trade_action_label.config(text="No Signal", foreground="yellow")

            self.draw_chart(self.trading_chart_frame, lambda: generate_stock_graph(self.current_stock))

        except Exception as e:
            print(f"Error encountered: {e}")  # Debugging
            self.stock_name_label.config(text=f"Error: {e}", foreground="red")

        if self.is_updating:
            self.root.after(3000, self.update_trading_helper)