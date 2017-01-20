## creates and allows the training of a neural model that can later be used by a strategy


from candle_table import CandleTable
from trend_cutter import TrendCutter
from trend_table import TrendTable
from sklearn.neural_network import MLPClassifier

TIME_PERIOD = 14400
FUTURE_DURATION = 5 ##used to determine outputs, how many days in the future is the avg computed
PAST_DURATION = 5 ##used to determine model inputs, how many days in the past will we look at the trend

class NeuralTrendModel:

	def __init__(self):
		self.num_future = FUTURE_DURATION * 86400/TIME_PERIOD
		self.num_past = PAST_DURATION * 86400/TIME_PERIOD
		self.model = MLPClassifier()
		self.outputs = []
		self.inputs = []

	def train_model(self, candle_table_name, trend_table_name):
		##get trends
		tc = TrendCutter(candle_table_name, trend_table_name)
		trend_table = tc.create_cut_table()
		trends = TrendTable.get_trend_array(trend_table.table_name)
		
		##use trends to get inputs
		self.inputs += self.get_inputs(trends)
		
		##get candles and use them to calculate outputs
		candles = CandleTable.get_candle_array(candle_table_name)
		self.outputs += self.get_outputs(candles)
		
		print len(self.inputs)
		print len(self.outputs)
		self.model.fit(self.inputs, self.outputs)


	##computes inputs to train the model
	##this consists of an list of lists of length num_trends_past
	def get_inputs(self, trends):
		inputs = []
		num_trends = len(trends)
		i = self.num_past
		while i < num_trends - self.num_future:
			inp = []
			for j in range(self.num_past):
				inp.append(trends[i- (self.num_past - j)].hits)
			inputs.append(inp)
			i += 1
		return inputs




	##computes and returns the outputs from a list of candles
	def get_outputs(self, candles):
		outputs = [] ## -1 means sell, 0 means do nothing, 1 = buy
		num_candles = len(candles)
		## skip first num_past and last num_future because history and future is required to compute outputs and inputs
		i = self.num_past
		##calculating output requires looking at a future avg, not defined for the last few candles so end before that
		while i < (num_candles - self.num_future):
			cur = candles[i].close ##current value of candle
			total = 0

			##calculate avg of next few candles
			for j in range(self.num_future):
				total += candles[i].close	
			avg = total/self.num_future

			##if avg>current output is 1 means buy, 0 means do nothing, -1 means sell
			if avg > cur:
				out = 1
			elif avg == cur:
				out = 0
			else:
				out = -1
			outputs.append(out)
			i += 1
		
		return outputs

