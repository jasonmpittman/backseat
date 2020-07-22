import subprocess

import platform

import os

class Agent:
	def __init__(self):
		self._platform = self.get_platform()


	def get_platform(self):
		plat = platform.system()
		if plat == "Darwin":
			return "MacOS"
		else:
			return plat


	'''
	This function takes in a command then executes the command.
	The results are then returned as as string.
	'''
	def run_command(self, command):
		command_list = command.split(" ")
		subprocess_result = subprocess.run(command_list, capture_output=True)
		string_result = subprocess_result.stdout.decode("utf-8")
		string_result =  string_result[:-1]
		return string_result


if __name__ == "__main__":
	A = Agent()
	res = A.run_command("ls -l")
	print(res)
	print(A._platform)
