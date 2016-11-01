
library(DBI)
library(RSQLite)
setwd("C:\\Users\\andrei\\dev\\Midas\\db")
con = dbConnect(RSQLite::SQLite(), dbname = "currencies.sqlite")
alltables = dbListTables(con)
##print(alltables)

##eth = dbGetQuery( con,'select date, close from CANDLE_USDT_ETH_1470628800_9999999999_14400' )
##etc = dbGetQuery( con,'select date, close from CANDLE_USDT_ETC_1470628800_9999999999_14400' )
##ltc = dbGetQuery( con,'select date, close from CANDLE_USDT_LTC_1470628800_9999999999_14400' )
##xmr = dbGetQuery( con,'select date, close from CANDLE_USDT_XMR_1470628800_9999999999_14400' )
##xmr_trend = dbGetQuery( con,'select date, hits from TREND_monero_table_1470628800_1477382400' )
btc_buy = dbGetQuery( con,"select date, price from TRADE_AVG_TREND_BTC_14400 where type = 'BUY_TYPE'" )
btc_sell = dbGetQuery( con,"select date, price from TRADE_AVG_TREND_BTC_14400 where type = 'SELL_TYPE'" )
##eth_trend = dbGetQuery( con,'select date, hits from ethereum_table_1470628800_1476432000' )
##eth_roc = dbGetQuery( con,'select date, value from USDT_ETH_1470628800_9999999999_14400___SIMPLE_ROC' )

btc = dbGetQuery( con,'select date, close from CANDLE_USDT_BTC_1470628800_9999999999_14400' )
btc_trend = dbGetQuery( con,'select date, hits from TREND_bitcoin_table_1470628800_1477814400' )

##comb1 = merge(x = eth, y = btc, by = "date") 

##offset btc by a mulitple of 1800
##eth$date[] <- eth$date[] - 518400 
##eth$close[] <- eth$close[] * 5
##eth_roc$value[] <- (eth_roc$value[] * 10) + 30

##comb2 = merge(x = eth, y = btc, by = "date") 

##comb3 = merge(x = eth, y = eth_trend, by = "date", all = TRUE) 

trend1 =  dbGetQuery( con,'select date, value from POINT_BTC_table___SIMPLE_AVG_3' )
trend2 =  dbGetQuery( con,'select date, value from POINT_BTC_table___SIMPLE_AVG_25' )

##plot(trend1[,'date'], trend1[,'hits'], type = 'l')
##par(new=TRUE)
##plot(trend2[,'date'], trend2[,'hits'], type = 'l', col = 'green')


##reg1 = lm(close.x ~ close.y, data = comb1)
##reg2 = lm(close.x ~ close.y, data = comb2)

##source("C:\\Users\\andrei\\dev\\Midas\\r_scripts\\btc_eth_corr.r")
