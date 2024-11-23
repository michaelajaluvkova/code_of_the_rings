from engeto import DataDownloads
from plotting import Plotting

start_date = '2022-01-01'
end_date = '2023-12-31'
initial_investment = 1000

downloader = DataDownloads()

data = downloader.main(start_date=start_date, end_date=end_date)
plot = Plotting()
plot.run_plot(start_date, end_date, data, initial_investment, first='BTC', second='SOL')


