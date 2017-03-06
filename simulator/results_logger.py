## logs results from trade simulator in a file


class ResultsLogger:
	def __init__(self, currency, cur_table_name, trends_table_name, time_start, time_end, avg_short, avg_long):
		self.currency = currency
		self.trends_table_name = trends_table_name
		self.cur_table_name = cur_table_name
		self.time_start = time_start
		self.time_end = time_end
		self.avg_short = avg_short
		self.avg_long = avg_long
		self.filename = "./results/" + currency + ".txt"
		self.line = "___________________________________________________________________________________________________________________________________________________\n"

	##called with the results of a instance, puts it in file
	def log(self, total_bought, total_spent, total_sold, net_worth, bits):
		print(self.filename)	
		fo = open(self.filename, "a")
		fo.write(self.line)
		fo.write(self.trends_table_name + "   " + self.cur_table_name + "\n")
		fo.write("Period: " + str(self.time_start) + " - " + str(self.time_end) + "\n")
		fo.write("Settings: " + "avg_short: " + str(self.avg_short) + " avg_long: " + str(self.avg_long) + "\n")
		fo.write("\n")
		fo.write("Results:" + "\n")
		fo.write("Total Bought: " + str(total_bought) + "\n")
		fo.write("Total Spent: " + str(total_spent) + "\n")
		fo.write("Total Sold: " + str(total_sold) + "\n")
		fo.write("Ended with: " + "\n")
		fo.write("Bits:" + str(bits) + "\n")
		fo.write("Net Worth:" + str(net_worth) + "\n")
		fo.write("Profit Percent: " + str(net_worth/total_spent) + "\n")
		fo.write(self.line)
		fo.close()


	


