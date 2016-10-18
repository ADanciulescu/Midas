plot(eth_roc[,'date'], eth_roc[,'value'], type = 'l')
par(new=TRUE)
plot(eth_trend[,'date'], eth_trend[,'hits'], type = 'l', col = 'green')
