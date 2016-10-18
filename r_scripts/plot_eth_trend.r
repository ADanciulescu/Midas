plot(eth[,'date'], eth[,'close'], type = 'l')
par(new=TRUE)
plot(eth_trend[,'date'], eth_trend[,'hits'], type = 'l', col = 'green')
