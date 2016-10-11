
library(DBI)
library(RSQLite)
setwd("C:\\Users\\andrei\\dev\\Midas\\db")
con = dbConnect(RSQLite::SQLite(), dbname = "currencies.sqlite")
alltables = dbListTables(con)
print(alltables)

eth = dbGetQuery( con,'select date, close from USDT_ETH_1470628800_9999999999_1800' )
btc = dbGetQuery( con,'select date, close from USDT_BTC_1470628800_9999999999_1800' )


comb1 = merge(x = eth, y = btc, by = "date") 

##offset btc by a mulitple of 1800
btc$date[] = btc$date[] - 3600

comb2 = merge(x = eth, y = btc, by = "date") 



reg1 = lm(close.x ~ close.y, data = comb1)
reg2 = lm(close.x ~ close.y, data = comb2)

