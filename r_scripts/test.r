library(DBI)
library(RSQLite)
setwd("C:\\Users\\andrei\\dev\\Midas\\db")
con = dbConnect(RSQLite::SQLite(), dbname = "currencies.sqlite")
alltables = dbListTables(con)
print(alltables)

eth = dbGetQuery( con,'select date, close from USDT_ETH_1470628800_9999999999_300' )
btc = dbGetQuery( con,'select date, close from USDT_BTC_1470628800_9999999999_300' )
comb = dbGetQuery(con, 'select USDT_ETH_1470628800_9999999999_300.close as eth_close, USDT_BTC_1470628800_9999999999_300.close as btc_close, USDT_ETH_1470628800_9999999999_300.date from USDT_ETH_1470628800_9999999999_300 inner join USDT_BTC_1470628800_9999999999_300 on (USDT_ETH_1470628800_9999999999_300.date = USDT_BTC_1470628800_9999999999_300.date)')
reg = lm(eth_close ~ btc_close, data = comb)

acf(eth, lag.max = NULL, type = c("correlation", "covariance", "partial"), plot = TRUE, na.action = na.fail, demean = TRUE)
