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
		subprocess_result = subprocess.run(command_list, capture_output=True, check=True)
		string_result = subprocess_result.stdout.decode("utf-8")
		string_error = subprocess_result.stderr.decode("utf-8")
		string_result =  string_result[:-1]
		return string_result, string_error

	def mac_get_updates_list(self):
		brew_command = 'brew outdated'
		macOS_command = 'softwareupdate -l'
		macOS_command_res, macOS_command_err = self.run_command(macOS_command)
		brew_command_res, brew_command_err = self.run_command(brew_command)
		return macOS_command_res +"\n" + macOS_command_err + brew_command_res + brew_command_err

if __name__ == "__main__":
	A = Agent()
	print(A._platform)
	print(A.mac_get_updates_list())
