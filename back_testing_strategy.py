import pandas as pd
import matplotlib.pyplot as plt
import backtrader as bt
import yfinance as yf

# data = yf .download('AAPL', start='2020-01-01', end='2023-01-01')
# data.to_csv('AAPL.csv')
#TODO: why use close here? 
#TODO: why self
#TODO: why check position DONE
#TODO: How it transformed the data
data = pd.read_csv('AAPL.csv', skiprows=3, header=None)
data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
data.set_index('Date', inplace=True)
data.index = pd.to_datetime(data.index)
# print(data.head())
data_feed = bt.feeds.PandasData(dataname = data)

class MovingAverageCrossover(bt.Strategy):
    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(self.data.close, period = 10)
        self.long_ma = bt.indicators.SimpleMovingAverage(self.data.close, period = 30)
        self.rsi = bt.indicators.RSI(self.data.close, period = 14)
    
    def next(self):
        if not self.position:
            if self.short_ma > self.long_ma and self.rsi < 40:
                self.buy()
        else:
            if self.short_ma < self.long_ma and self.rsi > 60:
                self.sell()
                
cerebro = bt.Cerebro()
cerebro.addstrategy(MovingAverageCrossover)
cerebro.adddata(data_feed)
cerebro.run()
cerebro.plot()