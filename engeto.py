import yfinance as yf
import pandas as pd
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

class DataDownloads:
    def __init__(self):
        blabla = []
    def get_top_10_cryptos(self):
        coins = cg.get_coins_markets(vs_currency='usd')
        sorted_coins = sorted(coins, key=lambda x: x['market_cap'], reverse=True)
        top_10 = [f"{coin['symbol'].upper()}-USD" for coin in sorted_coins[:10]]

        return top_10
        
    def get_top_10_cryptos_denca(self):
        coins = cg.get_coins_markets(vs_currency='usd')
        sorted_coins = sorted(coins, key=lambda x: x['market_cap'], reverse=True)
        top_10 = [coin['symbol'].upper().replace('-USD', '') for coin in sorted_coins[:10]]

        return top_10

    def usd_czk(self, start_date, end_date):
        data = yf.download('USDCZK=X', start=start_date, end=end_date)
        all_data = []

        for date, row in data.iterrows():
            all_data.append({
                'Date': date,
                'Close_exchange': row['Close'].item(),
            })

        close_data = pd.DataFrame(all_data)
        close_data['Date'] = close_data['Date'].dt.tz_localize(None)

        return close_data
    def get_sp500_tickers(self, start_date, end_date):
        sp500_data = yf.download('^GSPC', start=start_date, end=end_date)

        all_data = []
        for date, row in sp500_data.iterrows():
            all_data.append({
                'Date': date,
                'Index': 'S&P 500',
                'Stock Close': row['Close'].item(),
                'Stock Volume': row['Volume'].item()
            })

        structured_data = pd.DataFrame(all_data)

        return structured_data

    def yahoo_crypto_multiple_structured(self, currencies, start_date, end_date):
        all_data = []

        for currency in currencies:
            crypto_data = yf.download(currency, start=start_date, end=end_date)
            crypto_info = yf.Ticker(currency).info
            market_cap = crypto_info.get('marketCap', None)

            for date, row in crypto_data.iterrows():
                all_data.append({
                    'Date': date,
                    'Currency': currency.replace('-USD', ''),
                    #'Open': row['Open'].item(),
                    #'High': row['High'].item(),
                    #'Low': row['Low'].item(),
                    'Close': row['Close'].item(),
                    #'Adj Close': row['Adj Close'].item(),
                    'Volume': row['Volume'].item(),
                    'Market Cap': market_cap
                })

        structured_data = pd.DataFrame(all_data)
        return structured_data

    def download_inflation(self):
        df = pd.read_excel('inflace_CZ.xlsx')
        df.columns = ['Date', 'Cumulative Inflation CZ']
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%Y')

        all_data = []

        for _, row in df.iterrows():
            start_date = row['Date']
            end_date = pd.Timestamp(start_date.year, start_date.month, 1) + pd.offsets.MonthEnd(0)
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')

            for date in date_range:
                all_data.append({
                    'Date': date.strftime('%Y-%m-%d %H:%M:%S'),
                    'inflation_cz': row['Cumulative Inflation CZ']
                })

        daily_df = pd.DataFrame(all_data)

        return daily_df
    def timeline_events(self):
        df = pd.read_csv('timeline_events.csv')
        df['Date'] = df['Date'].str.extract(r'^(.*?)(?=\s*[-–]|$)')[0]

        valid_date_pattern = r'^[A-Za-z]+\s\d{1,2}$'
        df = df[df['Date'].str.match(valid_date_pattern)]

        df['single_date'] = df['Year'].astype(str) + ' ' + df['Date']
        df['single_date'] = pd.to_datetime(df['single_date'], format='%Y %B %d')

        data = df[['single_date', 'Event']]
        return data
        
    def merge_function(self, crypto, sp_500, inflation, exchange, events):
        merged_df = pd.merge(crypto, sp_500, on='Date', how='outer')
        merged_df['Stock Close'] = merged_df['Stock Close'].fillna(method='ffill')
        merged_df['Stock Volume'] = merged_df['Stock Volume'].fillna(method='ffill')
        merged_df['Stock Close'] = merged_df['Stock Close'].fillna(method='bfill')
        merged_df['Stock Volume'] = merged_df['Stock Volume'].fillna(method='bfill')

        merged_df['Index'] = merged_df['Index'].fillna(method='ffill')
        merged_df['Index'] = merged_df['Index'].fillna(method='bfill')
        merged_df['Date'] = pd.to_datetime(merged_df['Date'], errors='coerce')
        merged_df['Date'] = merged_df['Date'].dt.tz_localize(None)
        inflation['Date'] = pd.to_datetime(inflation['Date'], errors='coerce')

        merged_df = pd.merge(merged_df, inflation, on='Date', how='inner')
        merged_df = pd.merge(merged_df, exchange, on='Date', how='inner')
        merged_df['Close CZK'] = merged_df['Close'] * merged_df['Close_exchange']
        merged_df = pd.merge(merged_df, events, left_on='Date', right_on='single_date', how='left')
        merged_df = merged_df.drop(columns=['single_date'])

        return merged_df

    def main(self, start_date, end_date):
        down = DataDownloads()
        exchange = down.usd_czk(start_date, end_date)
        currencies = down.get_top_10_cryptos()
        crypto = down.yahoo_crypto_multiple_structured(currencies, start_date, end_date)

        sp_500 = down.get_sp500_tickers(start_date, end_date)
        inflation = down.download_inflation()
        events = down.timeline_events()
        merged_df = down.merge_function(crypto, sp_500, inflation, exchange, events)
        merged_df.to_csv('crypto_structured.csv', index=False)
        return merged_df
