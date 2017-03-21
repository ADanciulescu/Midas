## holds a set of tasks and runs them periodically
from task import Task
import traceback

class Scheduler:

	def __init__(self):
		self.tasks = []


	def run(self):
		task_num  = 0 ##index of task to run
		while(True):
			try:
				result = self.tasks[task_num].run()
			except Exception:
				print("************************************************ERROR IN TASK*********************************************************")
				result = Task.CONTINUE
				print(traceback.format_exc())

			if result == Task.DONE:
				print("deleted task")
				self.tasks.pop(task_num)
				task_num -= 1

			task_num += 1
			if task_num >= len(self.tasks):
				task_num  = 0

	def schedule_task(self, task):
		self.tasks.append(task)
