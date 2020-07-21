import os

class Agent:
	def __init__(self):
		self.run_command("ls -al")

	def run_command(self, command):
		test = os.system(command)
		print(test)

A = Agent()
