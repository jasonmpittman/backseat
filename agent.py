import subprocess

import platform

import os

import command_result

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
		try:
			command_list = command.split(" ")
			subprocess_result = subprocess.run(command_list, capture_output=True)
			string_result = subprocess_result.stdout.decode("utf-8")
			string_error = subprocess_result.stderr.decode("utf-8")
			exit_code = subprocess_result.returncode
			string_result =  string_result[:-1]
			res = command_result.Command_Result(string_result, string_error, exit_code)
		except BaseException as E:
			res = command_result.Command_Result("", f"Failed Command: {command}\n{E}", 1)
		return res


	def mac_get_updates_list(self):
		brew_command = 'brew outdated'
		macOS_command = 'softwareupdate -l'
		macOS_command_res, macOS_command_err = self.run_command(macOS_command)
		# brew_command_res, brew_command_err = self.run_command(brew_command)
		# return macOS_command_res +"\n" + macOS_command_err + brew_command_res + brew_command_err
		# return brew_command_res.split("\n")
		return "woo"

	def mac_brew_software_update(self, software_update):
		command = f"brew upgrade {software_update}"
		return self.run_command(command)

	def mac_brew_software_updates(self, software_list):
		output = ""
		for software in software_list:
			output_tup = self.mac_brew_software_update(software)
			output_list = list(output_tup)
			for part in output_list:
				output += part
		return output

if __name__ == "__main__":
	A = Agent()
	# print(A._platform)
	# print(A.mac_brew_software_updates(A.mac_get_updates_list()))
	res = A.run_command("woo")
	print(res.create_output())
