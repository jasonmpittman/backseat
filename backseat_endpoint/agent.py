import subprocess

import platform

import os

import getpass

import socket


#add success and failure responces

class Agent:
	"""
	The Agent handles all of the actual running of the commands.

	Attributes
	----------
	_platform : str
	"""
	def __init__(self):
		"""
		This sets up the Agent object.

		Parameters
		----------
		"""
		self._platform = self.get_platform()

	def get_platform(self):
		"""
		This function gets the OS of the endpoint.
		Parameters
		----------
		"""
		plat = platform.system()
		if plat == "Darwin":
			return "MacOS"
		else:
			return plat


	def run_command(self, command, password):
		"""
		This function takes in a command then executes the command.
		Then return stdout (str), stderr (str), ret_code (int)
		Parameters
		----------
		command : str
		"""
		command_list = command.split(" ")
		ret = False
		if "sudo" in command_list:
			subprocess_result = self._sudo_run_command(command_list, password)
		else:
			try:
				subprocess_result = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			except Exception as E:
				stdout = ""
				stderr = str(E)
				ret_code = 1
				return stdout, stderr, ret_code


		standard_out, standard_err = subprocess_result.communicate()
		ret_code = subprocess_result.returncode
		return standard_out.decode("utf-8"), standard_err.decode("utf-8"), subprocess_result.returncode

	def _sudo_run_command(self, command_list, password):
		"""
		This function runs the sudo commands. Currently not used.

		Parameters
		----------
		command_list : list
		"""
		print("-- SUDO NOT IMPLEMENTED DUE TO INSECURITY --")
		return
		if not "sudo" in command_list:
			return False
		command_list.insert(command_list.index("sudo")+1, "-S")
		print(command_list)
		subprocess_result = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		# subprocess_result.communicate(password.encode())
		subprocess_result.stdin.write(bytes(password, "utf-8"))
		return subprocess_result


if __name__ == "__main__":
	pass
