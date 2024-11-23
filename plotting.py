import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Plotting():
    def __init__(self):
        blabla = []

    def run_plot(self, start_date, end_date, data, initial_investment, first, second):
        if second == 'S&P 500':
            self.plot_crypto_stock(data, start_date, end_date, first_crypto=first, stock=second, initial_investment=initial_investment)
        else:
            self.plot_crypto(data, start_date, end_date, first_crypto=first, second_crypto=second, initial_investment=initial_investment)

    def plot_crypto(self, data, start_date, end_date, first_crypto, second_crypto, initial_investment):
        df1 = data[data['Currency'] == first_crypto]
        df2 = data[data['Currency'] == second_crypto]

        df1['Initial Investment'] = initial_investment

        df1['Shares Bought'] = df1['Initial Investment'] * df1['Close']
        start_date = df1['Date'].min()
        start_shares = df1[df1['Date'] == start_date]['Shares Bought'].iloc[0]
        df1['Percentage'] = ((df1['Shares Bought'] / start_shares) -1) * 100

        df2['Initial Investment'] = initial_investment
        df2['Shares Bought'] = df2['Initial Investment'] * df2['Close']
        start_date = df2['Date'].min()
        start_shares = df2[df2['Date'] == start_date]['Shares Bought'].iloc[0]
        df2['Percentage'] = ((df2['Shares Bought'] / start_shares) -1) * 100

        # Create the plot with two y-axes
        sns.set(style="whitegrid", palette="muted")
        fig, ax1 = plt.subplots(figsize=(12, 8))

        ax1.plot(df1['Date'], df1['Percentage'], color='blue', label=f"{first_crypto} Investment", linestyle='-', marker='o', markersize=5)
        ax1.set_xlabel("Date", fontsize=12, fontweight='bold')
        ax1.set_ylabel(f"{first_crypto} Investment Value (USD)", color='blue', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', colors='blue')
        ax1.set_xticks(df1['Date'][::int(len(df1)/5)])
        ax1.set_xticklabels(df1['Date'][::int(len(df1)/5)].dt.strftime('%Y-%m-%d'), rotation=45, fontsize=10)
        ax1.set_ylim(auto=True)

        ax2 = ax1.twinx()
        # Right graph (Investment Value of the stock)
        ax2.plot(df2['Date'], df2['Percentage'], color='red', label=f"{second_crypto} Investment", linestyle='-', marker='s', markersize=5)
        ax2.set_ylabel(f"{second_crypto} Investment Value (USD)", color='red', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', colors='red')
        ax2.set_ylim(auto=True)
        ax1.legend(title="Investment Growth", title_fontsize='13', fontsize='11', loc='upper left')
        ax2.legend(title="Investment Growth", title_fontsize='13', fontsize='11', loc='upper right')

        # Title and layout
        plt.title(f"Investment Growth of {first_crypto} & {second_crypto} Over Time\nInitial Investment: {initial_investment} USD", fontsize=16, fontweight='bold', color='darkblue', pad=20)
        plt.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()
        plt.savefig('media/crypto.png')
        plt.show()


    def plot_crypto_stock(self, data, start_date, end_date, first_crypto, stock, initial_investment):
        df1 = data[data['Currency'] == first_crypto]
        print(df1.head())

        df1['Initial Investment'] = initial_investment

        df1['Shares Bought'] = df1['Initial Investment'] * df1['Close']
        start_date = df1['Date'].min()
        start_shares = df1[df1['Date'] == start_date]['Shares Bought'].iloc[0]
        df1['Percentage'] = ((df1['Shares Bought'] / start_shares) -1) * 100

        df1['Shares Bought Stock'] = df1['Initial Investment'] * df1['Stock Close']
        start_date = df1['Date'].min()
        start_shares = df1[df1['Date'] == start_date]['Shares Bought Stock'].iloc[0]
        df1['Percentage Stock'] = ((df1['Shares Bought Stock'] / start_shares) -1) * 100


        df1.to_csv('df.csv')


        # Create the plot with two y-axes
        sns.set(style="whitegrid", palette="muted")
        fig, ax1 = plt.subplots(figsize=(12, 8))

        # Left graph (Investment Value of the first crypto)
        ax1.plot(df1['Date'], df1['Percentage'], color='blue', label=f"{first_crypto} Investment", linestyle='-', marker='o', markersize=5)
        ax1.set_xlabel("Date", fontsize=12, fontweight='bold')
        ax1.set_ylabel(f"{first_crypto} Investment Value (USD)", color='blue', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='y', colors='blue')
        ax1.set_xticks(df1['Date'][::int(len(df1)/5)])  # Display a subset of dates for clarity
        ax1.set_xticklabels(df1['Date'][::int(len(df1)/5)].dt.strftime('%Y-%m-%d'), rotation=45, fontsize=10)
        ax1.set_ylim(auto=True)

        ax2 = ax1.twinx()
        # Right graph (Investment Value of the stock)
        ax2.plot(df1['Date'], df1['Percentage Stock'], color='red', label=f"{stock} Investment", linestyle='-', marker='s', markersize=5)
        ax2.set_ylabel(f"{stock} Investment Value (USD)", color='red', fontsize=12, fontweight='bold')
        ax2.tick_params(axis='y', colors='red')
        ax2.set_ylim(auto=True)
        ax1.legend(title="Investment Growth", title_fontsize='13', fontsize='11', loc='upper left')
        ax2.legend(title="Investment Growth", title_fontsize='13', fontsize='11', loc='upper right')

        # Title and layout
        plt.title(f"Investment Growth of {first_crypto} & {stock} Over Time\nInitial Investment: {initial_investment} USD", fontsize=16, fontweight='bold', color='darkblue', pad=20)
        plt.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()
        plt.savefig('media/crypto.png')
        plt.show()
        
