
library(DBI)
library(RSQLite)
setwd("C:\\Users\\andrei\\dev\\Midas\\db")
con = dbConnect(RSQLite::SQLite(), dbname = "currencies.sqlite")
alltables = dbListTables(con)
print(alltables)

eth = dbGetQuery( con,'select date, close from USDT_ETH_1470628800_9999999999_14400' )
btc = dbGetQuery( con,'select date, close from USDT_BTC_1470628800_9999999999_14400' )
eth_trend = dbGetQuery( con,'select date, hits from ethereum_table_1470628800_1476432000' )
avg = dbGetQuery( con,'select date, value from USDT_BTC_1470628800_9999999999_14400___EXP_AVG' )
eth_roc = dbGetQuery( con,'select date, value from USDT_ETH_1470628800_9999999999_14400___SIMPLE_ROC' )

comb1 = merge(x = eth, y = btc, by = "date") 

##offset btc by a mulitple of 1800
btc$date[] = btc$date[] - 3600

comb2 = merge(x = eth, y = btc, by = "date") 

comb3 = merge(x = eth, y = eth_trend, all = TRUE) 



##reg1 = lm(close.x ~ close.y, data = comb1)
##reg2 = lm(close.x ~ close.y, data = comb2)

##source("C:\\Users\\andrei\\dev\\Midas\\r_scripts\\btc_eth_corr.r")
