library(ggplot2)
##library(gridExtra)
##plot(eth[,'date'], eth[,'close'], type = 'l')
##par(new=TRUE)
##plot(eth_trend[,'date'], eth_trend[,'hits'], type = 'l', col = 'green')
	g1 =ggplot() + 
	geom_line(data=btc, aes(x=date, y=close), color='green') +
	geom_line(data=btc_trend, aes(x=date, y=hits), color='red')


 ##p1 <- ggplot_gtable(ggplot_build(p1))
 ##p2 <- ggplot_gtable(ggplot_build(p2))

 ##maxWidth = grid::unit.pmax(p1$widths[2:3], p2$widths[2:3])
 
 ##p1$widths[2:3] <- maxWidth
 ##p2$widths[2:3] <- maxWidth



##grid.arrange(p1, p2, heights = c(3, 2))
