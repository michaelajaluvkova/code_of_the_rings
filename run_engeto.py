from engeto import DataDownloads
start_date = '2023-01-01'
end_date = '2023-12-31'

downloader = DataDownloads()

data = downloader.main(start_date=start_date, end_date=end_date)

print("Data has been successfully processed and saved to 'crypto_structured.csv'")
print(data.head())
print(data.columns)