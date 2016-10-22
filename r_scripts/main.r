
library(DBI)
library(RSQLite)
setwd("C:\\Users\\andrei\\dev\\Midas\\db")
con = dbConnect(RSQLite::SQLite(), dbname = "currencies.sqlite")
alltables = dbListTables(con)
print(alltables)

eth = dbGetQuery( con,'select date, close from CANDLE_USDT_ETH_1470628800_9999999999_14400' )
##eth_trend = dbGetQuery( con,'select date, hits from ethereum_table_1470628800_1476432000' )
##eth_roc = dbGetQuery( con,'select date, value from USDT_ETH_1470628800_9999999999_14400___SIMPLE_ROC' )

##comb1 = merge(x = eth, y = btc, by = "date") 

##offset btc by a mulitple of 1800
##eth$date[] <- eth$date[] - 518400 
##eth$close[] <- eth$close[] * 5
##eth_roc$value[] <- (eth_roc$value[] * 10) + 30

##comb2 = merge(x = eth, y = btc, by = "date") 

##comb3 = merge(x = eth, y = eth_trend, by = "date", all = TRUE) 

trend2 =  dbGetQuery( con,'select date, value from POINT_ethereum_table___SIMPLE_AVG_2' )
trend5 =  dbGetQuery( con,'select date, value from POINT_ethereum_table___SIMPLE_AVG_5' )


##reg1 = lm(close.x ~ close.y, data = comb1)
##reg2 = lm(close.x ~ close.y, data = comb2)

##source("C:\\Users\\andrei\\dev\\Midas\\r_scripts\\btc_eth_corr.r")
