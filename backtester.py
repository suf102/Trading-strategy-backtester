import yfinance as yf
import pandas   as pd
import numpy    as np
import random
from numba import jit, njit, types, vectorize, prange
import plotly.express as plt
import fundamentalanalysis as fa

# This function will get the price data from Yfinance and place it into a pandas dataframe.

def getdata(stockname,testperiod, datatype, interval1):
    yfdata = yf.Ticker("{}".format(stockname)).history(period=str(testperiod),interval = interval1)
    closedata = yfdata[datatype].copy()
    return closedata

# This will backtest liquidating the position when a sell signal is sent and spending all available cash when a buy signal is sent. 
# It will then calculate the calmative protfolio value.

def backtester(signals,price, tcost = 0.001):

    pos_val = np.zeros(np.shape(price))
    cash    = np.zeros(np.shape(price))
    cash[0] = 1
    
    #loop through each day as though we are going through and actually implementing the strategy as we go

    for i,val in enumerate(price):
        
        #if we are on the last day exit the loop we are done.

        if i == len(price)-1:
            break
        
        # if the signal that that day is to sell the on the next day we should have the possible value of the security, 
        # times the price of the security times the brokerage costs plus the money we had perviously.
        # We also sell all of the security that we have so the possible value left to us is zero

        if signals[i] == -1:

            cash[i+1] = (pos_val[i] * val * (1-tcost)) + cash[i]
            pos_val[i+1] = 0
            
        #If the signal that day is to buy, what we will do is take all of the cash that we have, divide it by the cost of the security to work out how many we can buy
        #factoring in the cost of the brockerage, we then add it to any stock we held from the pervious day

        elif signals[i] == 1:

            pos_val[i+1] = (cash[i] / val)*((1-tcost)) + pos_val[i]
            cash[i+1] = 0
            
        # Lastly we need to define the do nothing clause. this will not make a buy or a sell, we do need to update the position value to be the number of stocks/securitys we own times that days price
            
        elif signals[i] == 0:
            
            pos_val[i+1] = pos_val[i]/price[i]*price[i+1]
            cash[i+1] = cash[i]
            
    #then our returns are the amount of cash left each day plus the the price times the amoint of coin that we have

    returns = [a*b for a,b in zip(pos_val,price)] + cash
    
    #lastly we turn this into a data frame too
    
    return pd.DataFrame(returns, index = price.index)

#Similar to the backtester above, this backterter will not hold cash, rather it will hold US trasury Tbills at their present value.
#Note that this backtester will only work over monthly data as it is set up for holding those TBills for one month.


def backtestert(signals,price,tbill ,  tcost = 0.001,):

#Make a quick numpy array to save the money that will be made for possible value that the stock could be sold at and the cash on hand, start with one dollar so its not empty.

        pos_val = np.zeros(np.shape(price))
        cash    = np.zeros(np.shape(price))
        cash[0] = 1
        
        #loop through each day as though we are going through and actually implementing the strategy as we go

        for i,val in enumerate(price):
            
            #if we are on the last day exit the loop we are done.

            if i == len(price)-1:
                break
            
            # The number we are given for the 3 month bill is the annualized yield, however we might only want to hold this bill for a month, so we need to work out the monthly returns on the bill.

            if signals[i] == -1:

                cash[i+1] = (pos_val[i] * val * (1-tcost)) + cash[i]*(1+(tbill[i]/12)/100)
                pos_val[i+1] = 0
                
            #If the signal that day is to buy, what we will do is take all of the cash that we have, divide it by the cost of the security to work out how many we can buy
            #factoring in the cost of the brockerage, we then add it to any stock we held from the pervious day

            elif signals[i] == 1:

                pos_val[i+1] = (cash[i] / val)*((1-tcost)) + pos_val[i]
                cash[i+1] = 0

        #then our returns are the amount of cash left each day plus the the price times the amount of the security that we have

        returns = [a*b for a,b in zip(pos_val,price)] + cash
        
        #lastly we turn this into a data frame too
        
        return pd.DataFrame(returns, index = price.index)
    
# This function calculates the true positive win rate of of a strategy, i.e. how many times did a positive buy signal result in an increase in the portfolio value in the next period, divided by the number positive buy signals did we get
    
def winrate(data,returns):

#make an empty list to store the number of trades made that were money making. 

    tps = []

    #take all of the signals excluding the first and last ones

    sigs = data['Signals'][1:-1].values.ravel()

    #take the percentage returns day on day, not sure why we are only including the days where there is some kind of buy trade and not a sell trade

    rets = (returns.pct_change()).shift(1).dropna().values.ravel()

    #Record a positive signal every time a trade is made and it results in a positive return.
    
    for i,val in enumerate(sigs):  
        if (sigs[i] == 1 and rets[i]>0):
            tps.append(1)

    #Possible other signals that might result in gain, such as holding or selling.

#        if (sigs[i] == -1 and rets[i]>0):
#            tps.append(1)
#        if (sigs[i] == 0 and rets[i]>0):
#            tps.append(1)

    # work out the number of posative signals

    signals, counts = np.unique(sigs, return_counts=True )
    possignals = dict(zip(signals,counts))[1]

    #take the number of buy signals that result in a positive return the next day and divide it by the total number of positive signals to work out hte true positive score.

    win_rate = sum(tps)/possignals
    return win_rate

# The sharpe ratio works out the retuns 

def Sharperatio(returns,tradingdays,rrr):
    
    #First thing to do is to work out the percentage change in the returns for the last year, note that depending on what we are trading there
    #might be a different number of trading days, in the case of Bitcoin the default there are 365, for stocks it is usually 255
    
    lastyearreturns = returns.tail(tradingdays).pct_change().dropna()
    
    # Then working out the sharpe ratio, which is defined as the annualized rate of return minus the guaranteed rate of return divided by the standard deviation
    # of hte returns we need to make sure that we multiply by the 
    
    # Note that we are multiplying the standard deviation by the square root of the trading days, this is because it needs to be the annualized
    # Standard deviation, the daily rate.

    
    sharperatio = (lastyearreturns.mean() * tradingdays - rrr)/(lastyearreturns.std()* np.sqrt(tradingdays))
    
    return sharperatio 

# The Maximum Drawdown is the maximum percentage decrease in value from the most recent peak to the current price across the whole testing period. 
# This is a measure of how much one could loose if they implemented this strategy at the peak and exited at the bottom.

def MDD(returns):
    
    #To work out the maximum draw down we need to find the most recent peak. 
    
    RollingMaximum = returns.rolling(returns.shape[0],min_periods=1).max()
    
    # Then work out the percentage loss in returns between the peak at the current period
            
    DailyDrawdown = (returns-RollingMaximum)/RollingMaximum
    
    #Find the maximum(minimum because we are looking for the biggest decrease) drop across the whole back testing period.  
        
    MaximumDrawDown = DailyDrawdown.min()
    
    return MaximumDrawDown
    
