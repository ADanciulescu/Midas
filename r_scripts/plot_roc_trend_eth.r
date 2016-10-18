##plot(eth_roc[,'date'], eth_roc[,'value'], type = 'l')
##par(new=TRUE)
##plot(eth_trend[,'date'], eth_trend[,'hits'], type = 'l', col = 'green')
library(ggplot2)
##library(gridExtra)
##plot(eth[,'date'], eth[,'close'], type = 'l')
##par(new=TRUE)
##plot(eth_trend[,'date'], eth_trend[,'hits'], type = 'l', col = 'green')
g1 =ggplot() + 
geom_line(data=eth_roc, aes(x=date, y=value), color='green') +
geom_line(data=eth_trend, aes(x=date, y=hits), color='red')
