import subprocess

import sys


class Agent:
	def __init__(self):
		pass

	'''
	This function takes in a command then executes the command.
	The results are then returned as as string.
	'''
	def run_command(self, command):
		command_list = command.split(" ")
		subprocess_result = subprocess.run(command_list, stdout=subprocess.PIPE)
		string_result = subprocess_result.stdout.decode("utf-8")
		return string_result

A = Agent()
A.run_command("ls -l")
