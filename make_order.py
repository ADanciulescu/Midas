from order_maker import OrderMaker

om = OrderMaker()
om.slow_sell("BTC", 1, sell_all = True)
om.slow_sell("ETH", 1, sell_all = True)
