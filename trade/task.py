## subroutine that gets called by scheduler
## performs an action (sell/buy/update)
## specified by function that gets passed in

import time

class Task:

	DONE = "DONE"
	CONTINUE = "CONTINUE"
	
	def __init__(self, func, freq, args):
		self.freq = freq ##frequency at which to run the function code
		self.func = func ## function representing the code the task is supposed to run
		self.args = args ## arguments for the task's function
		self.last_run_time = 0

	
	def run(self):
		cur_time = time.time()
		if (cur_time - self.last_run_time)> self.freq:
			self.last_run_time = cur_time
			return self.func(*self.args)
		else:
			return Task.CONTINUE
