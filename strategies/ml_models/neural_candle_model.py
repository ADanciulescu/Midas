## creates and allows training of neural network model
## input is array of close histories of candles
## output is array of 1 or 0  or -1 corresponding to buy , nothing, sell



from candle_table import CandleTable
from sklearn.neural_network import MLPClassifier

TIME_PERIOD = 14400
FUTURE_DURATION = 5 ##used to determine outputs, how many days in the future is the avg computed
PAST_DURATION = 5 ##used to determine model inputs, how many days in the past will we look at the candle closing history 

class NeuralCandleModel:
	
	##mode of operation, what attribute to use as inputs
	CLOSE = "close"
	VOLUME = "volume"

	def __init__(self, mode):
		self.mode = mode
		self.num_future = FUTURE_DURATION * 86400/TIME_PERIOD
		self.num_past = PAST_DURATION * 86400/TIME_PERIOD
		self.model = MLPClassifier()
		self.outputs = []
		self.inputs = []

	def train_model(self, candle_table_name):
		
		##get candles and use them to calculate outputs
		candles = CandleTable.get_candle_array(candle_table_name)
		
		##use candles to get inputs
		self.inputs += self.get_inputs(candles)
		
		self.outputs += self.get_outputs(candles)
		
		self.model.fit(self.inputs, self.outputs)


	##computes inputs to train the model
	##this consists of an list of lists of length num_past
	def get_inputs(self, candles):
		inputs = []
		num_candles = len(candles)
		i = self.num_past
		while i < num_candles - self.num_future:
			inp = []
			for j in range(self.num_past):
				if self.mode == self.CLOSE:
					inp.append(candles[i- (self.num_past - j)].close)
				elif self.mode == self.VOLUME:
					inp.append(candles[i- (self.num_past - j)].volume)
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

