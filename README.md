# Midas

<h2>Project Goal:</h2>

1. Use a bot to put into practice a cryptotrading strategy that consistently outperforms market. 


<h2>Project Functions:</h2>

1. Historical data fetching from Poloniex cryptotrading exchange
2. Backtesting trading strategies against historical data.
3. Live application of strategies on the exchange.

<h2>Project Structure:</h2>
  1. ./Models/ Contains definitions of self contained packages of data which are stored on persistent storage(sqlite).<br>
  Models provide a standardized interface between the data in db and the code using the data. <br>
  Meaning, when data is fetched, it is assembled into a corresponding model and saved to db.<br>
  Likewise, data is retrieved from db in the form of objects of the corresponding model type. Examples:  <br>
    Candle: A candle object stores all the fields used to define a candlestick --a snapshot of the price during a x minute trading window--<br>
    Trend: A trend object stores data pertaining to a google trend snapshot for a given currency <br>
    ...<br>
    
 2. ./data_fetchers/ Code used to fetch data from without. Data is converted into models and saved to db.
    candle_fetcher fetches candle stick data from polo. <br>
    trend_fetcher fetches trend data from google. <br>
    trade_fetcher fetches users trading history.<br>
    ...
    
 3. ./data_parsers/ Converts raw API data into standards defined in Models
 
 4. ./exchange_clients/ Interface used by bot to actively trade on exchange. Note Bitfinex client is not finished.
 
 5. ./point_creators/ Sometimes, the implementation of various TA techniques required the computation of intermediary data points. <br>
 For example, points corresponding to moving averages. ./point_creators/ stores code for computing these intermediary points which are converted <br>
 to Point model and stored persistently in db.
 
 6. ./r_scripts/ Stores some R code, that I used to visualize and mess around with data.
 
 7. ./scripts/ misc scripts used to synch up remote server db with local, etc.
 
 8. ./simulation. Main file is trade_simulator.py. If specific trading strategies are like game cartridges, trade_simulator is like the nintendo console.<br>
 Takes as input a trading strategy and historical data of a currency and simulates trading based on that strategy. Output is the performance.<br>
 Contains some other code as well for modifying parameters of strategies and logging results in db.
 
 9. ./strategies/ Contains the implementation of various strategies. Main method of each strategy is decide which given a specific point in time will decide whether to buy or sell. 
 Each strategy should be compatile with both the exchange code that buys/sells live, and the simulator code.
 
 10. ./trade/ Code rand on remote server used to perform live trades on the exchange. Makes use of a specific strategies to decide when to buy/sell.
 
 11. ./tools/ misc stuff, hard coded table names, random general purpose code.
 
 
 <h2>TODO:</h2>
 1. Backtest my old strategies to see if they holdup in light of a whole bunch of new data.
 
 2. Work on half-done parallel project called Argos that uses js to visualize trades. <br>
 This should give insight into the shortcomings of backtesting as a whole as well as where specific strategies go wrong.
 
 3. Come up with new strategies. General af but I got some ideas.
 
 4. Add different exchange clients other than poloniex since others may have advatanges such as lower fees/
 
 5. Look into possibility for arbitrage between exchanges.
 
  <h2>How to run:</h2>
   <h3>Fetch Data:</h3>
      python3 pull_data.py --ticker BTC --start_date 2019-1-1 --resolution 300
   <h3>Backtest Strategy against existing data:</h3>
      python3 backtest.py --strategy BollingerStrategy --ticker BTC --start_date 2019-06-01 --resolution 300 --num_days 100
