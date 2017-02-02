
library(DBI)
library(RSQLite)
setwd("C:\\Users\\andrei\\dev\\Midas\\db")
con = dbConnect(RSQLite::SQLite(), dbname = "currencies.sqlite")
alltables = dbListTables(con)
##print(alltables)

##eth = dbGetQuery( con,'select date, close from CANDLE_USDT_ETH_1475280000_9999999999_14400' )
##etc = dbGetQuery( con,'select date, close from CANDLE_USDT_ETC_1475280000_9999999999_14400' )
##ltc = dbGetQuery( con,'select date, close from CANDLE_USDT_LTC_1475280000_9999999999_14400' )
##xmr = dbGetQuery( con,'select date, close from CANDLE_USDT_XMR_1475280000_9999999999_14400' )
##xmr_trend = dbGetQuery( con,'select date, hits from TREND_monero_table_1475280000_1477382400' )
##btc_buy = dbGetQuery( con,"select date, price from TRADE_AVG_TREND_BTC_14400 where type = 'BUY_TYPE'" )
##btc_sell = dbGetQuery( con,"select date, price from TRADE_AVG_TREND_BTC_14400 where type = 'SELL_TYPE'" )
##eth_trend = dbGetQuery( con,'select date, hits from ethereum_table_1475280000_1476432000' )
##eth_roc = dbGetQuery( con,'select date, value from USDT_ETH_1475280000_9999999999_14400___SIMPLE_ROC' )

btc = dbGetQuery(con,'select date, close from CANDLE_USDT_BTC_1475280000_9999999999_14400')
btc_vol = dbGetQuery(con,'select date, volume from CANDLE_USDT_BTC_1475280000_9999999999_14400')
btc_trend = dbGetQuery( con,'select date, hits from TREND_BTC_table_1475280000_1484899200' )
eth = dbGetQuery(con,'select date, close from CANDLE_USDT_ETH_1475280000_9999999999_14400')
eth_vol = dbGetQuery(con,'select date, volume from CANDLE_USDT_ETH_1475280000_9999999999_14400')
eth_trend = dbGetQuery( con,'select date, hits from TREND_ETH_table_1475280000_1484899200' )
xmr = dbGetQuery(con,'select date, close from CANDLE_USDT_XMR_1475280000_9999999999_14400')
xmr_trend = dbGetQuery( con,'select date, hits from TREND_XMR_table_1475280000_1484899200' )

btc_boll_low = dbGetQuery(con,'select date, value from POINT_USDT_BTC_1475280000_9999999999_14400___SIMPLE_AVG_20_LOW')
btc_boll_high = dbGetQuery(con,'select date, value from POINT_USDT_BTC_1475280000_9999999999_14400___SIMPLE_AVG_20_HIGH')

##plot(btc[,'date'], btc[,'close'], type = 'l') 
##plot(eth[,'date'], eth[,'close'], type = 'l') 


##comb1 = merge(x = eth, y = btc, by = "date") 

##offset btc by a mulitple of 1800
##eth_trend$date[] <- eth_trend$date[] + 518400 
##btc$date[] <- btc$date[] - 518400 
##eth$close[] <- eth$close[] * 5
##eth_roc$value[] <- (eth_roc$value[] * 10) + 30

##comb2 = merge(x = eth, y = btc, by = "date") 

comb_btc = merge(x = btc, y = btc_trend, by = "date") 
comb_eth = merge(x = eth, y = eth_trend, by = "date") 
comb_xmr = merge(x = xmr, y = xmr_trend, by = "date") 

##trend1 =  dbGetQuery( con,'select date, value from POINT_BTC_table___SIMPLE_AVG_3' )
##trend2 =  dbGetQuery( con,'select date, value from POINT_BTC_table___SIMPLE_AVG_25' )

##plot(trend1[,'date'], trend1[,'hits'], type = 'l')
##par(new=TRUE)
##plot(trend2[,'date'], trend2[,'hits'], type = 'l', col = 'green')


reg_btc = lm(close ~ hits, data = comb_btc)
reg_eth = lm(close ~ hits, data = comb_eth)
reg_xmr = lm(close ~ hits, data = comb_xmr)
##reg2 = lm(close.x ~ close.y, data = comb2)

##source("C:\\Users\\andrei\\dev\\Midas\\r_scripts\\btc_eth_corr.r")
