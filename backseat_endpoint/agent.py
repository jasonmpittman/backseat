import subprocess

import platform

import os

import getpass

import socket


#add success and failure responces

class Agent:
	def __init__(self):
		self._platform = self.get_platform()
		# self._ip = socket.gethostbyname(socket.gethostname())


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
		ret = False
		if "sudo" in command_list:
			print("Going to run sudo command")
			subprocess_result = self._sudo_run_command(command_list)
		else:
			subprocess_result = subprocess.Popen(command_list, stdout=subprocess.PIPE)

		output = subprocess_result.communicate()[0]

		return output.decode("utf-8"), subprocess_result.returncode

	def _sudo_run_command(self, command_list):
		if not "sudo" in command_list:
			return False
		command_list.insert(command_list.index("sudo")+1, "-S")
		print(command_list)
		password = getpass.getpass("|Password: ")
		subprocess_result = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		# subprocess_result.communicate(password.encode())
		subprocess_result.stdin.write(bytes(password, "utf-8"))
		return subprocess_result

	
if __name__ == "__main__":
	A = Agent()
	print(A._platform)
	print("--")
	print(A.run_command("sudo ls -al"))
	print("--")
	# print(A.ubuntu_get_updates_list())
	# print("-- Release information --")
	# print(A.run_command("lsb_release -a"))

	# res = A.run_command("pip3 install cryptography")
	# print(res)
	# print(A._platform)
	# print(A.mac_brew_software_updates(A.mac_get_updates_list()))

	# res = A.mac_brew_software_updates(["hugo"])
	# print(res)

	# res = A.run_command("./hugo.zsh")
	# print(res.create_output())

	# A.mac_os_install("10.14.6")
	#10.14.6
