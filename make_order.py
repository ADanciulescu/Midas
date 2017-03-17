from order_maker import OrderMaker
import time

om = OrderMaker()
time.sleep(5)
##om.slow_buy("XRP", 1, sell_all = True)
om.slow_sell("ETH", 1)
