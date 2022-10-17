# Trading Strategy Backtester

I have coded up a backtester you can use to see how different trading strategies work and how well they will perform. This was originally based on the backtester by @filthyquant on tiktok.
I have tried to comment the code in such a way that someone with relatively little familiarity with code could try and adapt or add their own strategies. If someone isn't interested in the code there is a section near the bottom where all of the parameters can be changed, just edit as your please and run all. 
(Bonus: at the very bottom there is a cell that will execute the coin flip strategy n times and averages the results, so convince yourself on its results on average.)

### Note: This is not an endorsement of technical analysis, rather this is simply an interactive piece to let people see how those strategies would fare with various parameters.

### Edit I have added in a absolute momentum strategy based on this paper https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2244633. This can be found in a separate notebook entitled Momentum_strategy.ipynb .  
## The strategies 

### Simple moving average (SMA)
A simple moving average strategy is one which takes the previous days and works out an average, if the price goes above this average you buy if it drops below you sell. 
I have also included a parameter that allows you to tune how much the moving average needs to go above the price to trigger a buy or a sell, this was done mainly so that you don’t end up with too many trades. 
### Expnenial moving average (EMA)
Very similar to the simple moving average, this strategy takes the previous n days worth of data and averages them, but it gives more weight to the more recent days. 
As with he simple average if the price is above the EMA then you buy, if the price is below you sell. 
### Crossover moving strategy (XMA)
In this strategy we take two simple averages, one over a short period, and one over a long period.
When the short period average is above the long we take this as a sign that the price will be trending up and we buy, similarly when the price is below we sell. 
This is designed to take out some of the noise of the simple approach as it wont send a signal based on just a single day if the movement isn’t very large.
### Relative strength index  (RSI)
The relative strength index of a security is a number between 1-100 that is designed to security if a stock is being overbought or over sold relative some mean. 
If the number is higher i.e. above 70, then it is likely the security is overbought. 
Therefore, it would not be a good time to buy as the price is likely to drop when people realize this. 
Similarly, when the number is low i.e. below 30 it might be a good time to buy as the security as you might expect a price jump. 
### Coin flip
Lastly as just a bit of fun I have included a coin flip, where you can set the percentages chance to buy sell or hold. 
This is really to show how in some situations these strategies may be no better than just random buying and selling. 

## The parameters 
If you are looking to just see how different parameters will affect the returns and win rates these are the only things you need to concern yourself with, they are paced after the strategies in the notebook. 

Stockname: here put the name of the security you would like to use as an example, use the standard ticker with quotes around the outside.

Testperiod: how far back do you want to test, standard syntax, 1m, 30d, 30y etc.

Datatype: Which data do you want to pull, the tester is currently only set up to use one bit of data from each period, I would suggest ‘Close’

interval1: The period of data that we want to consider, for the week end close or day close etc. 

rrr: The risk free rate of return, the rate of return that we would expect from an asset that has no risk, typically this is the us 10 year treasury bond for the relevent period. 

tradingdays: The number of days that the the stock that we are using is traded, it might be 365 for some stocks 255 for those only traded on weekdays.

Tcost: this parameter adds in a transaction cost on each trade as a percentage of the trade, 0.01 would be a 1% transaction cost.

Shortdays: this number is the number of days in the simple moving average, exponential moving average and the moving crossover strategy

Longdays: this number is the long average in the moving crossover strategy.

Toll: this number lets you set as a percentage the amount that a price or average needs to go above another to trigger a trade, you might want to set this as it will reduce the number of trades and thus alpha lost to trading costs. 

Rsi_period: this is the number of days that the relative strength index is calculated for, typically 14 is used. 

Overbuy: this is the threshold above which the security is being “overbought” between 0-100

Oversell: this is the threshold below which we might think the security is being “oversold” between 0-100, must be below over buy. 

Probbuy: for the coin filp chance of buying between 0-1. 

Probsell: for the coin filp the chance of selling between 0-1.

Probdonothing: for the coin flip the chance of doing nothing.

## Signals 
Each of these strategies will produce signals, either 1 for buy, 0 for do nothing or -1 for sell. The original back tester only had sma and buy or sell. 
But, given that I have introduced transaction costs to the model, It is important to add do nothing otherwise it gives an unrealistic impression where returns can be lost to just buying and selling with no return, an unrealistic scenario. 
## The backtester, 
The backtester simply implements the strategies and keeps a running total of the cash and position value when following the strategy. I use as starting cash of 1 just to makes the returns calculations easier. 

## Results
Here I will explain what the backtester will output, based on the meta parameters.
### Returns

The backtester will output the returns on 1 cash being put from the start of the test to "today"

### Win rates

The win rate takes the number of buy signals and after a buy signal does your returns value increase. It works out the percentage of times you get a positive return after a buy signal. This is the true positive ratio. Arguably this number is more important than the win rate. Given that is generally easy to improve your position in a bull market the win rate will eliminate some of the timing luck that the returns number will show.

### Sharpe ratio

The Sharpe ratio of a strategy is a ratio that expressed the difference between the guaranteed rate of return and returns from the strategy in question. Formally it is annualized rate of return minus the garenteed rate of return (often the annual return on US 10 year treasury bonds, but in this case it is just entered by the user) divided by the annualized standard deviation. 

## The graphs

I have included these to show how the retuns will change over time with SMA, EMA and XMA. I have also included the the RSI at any given time, and lastly a graph of the close price with the various moving averages superimposed on top. 

## Bonus 
The coin filp might do really well or really badly when you run it, so to get an average at the bottom of the notebook there is a cell that will run the coin flip 1000 times just to work out some averages. 

## Additional work
First, I think this would be a prime candidate for mercury interactive webpage for people to tweak perameters to see the results, circumventing the code part. 

Second, Jit or multipool could be used to speed up some of the calculations.\
