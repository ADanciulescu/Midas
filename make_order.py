from order_maker import OrderMaker
import time

om = OrderMaker()
time.sleep(5)
om.slow_sell("XRP", 1, sell_all = True)
