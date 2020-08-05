import subprocess

import platform

import os

import getpass

import socket


#add success and failure responces

class Agent:
	def __init__(self):
		self._platform = self.get_platform()
		self._ip = socket.gethostbyname(socket.gethostname())


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
		return output.decode("utf-8")

	def _sudo_run_command(self, command_list):
		if not "sudo" in command_list:
			return False
		command_list.insert(command_list.index("sudo")+1, "-S")
		print(command_list)
		password = getpass.getpass("|Password: ")
		subprocess_result = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		subprocess_result.communicate(password.encode())
		return subprocess_result

	def mac_get_updates_list(self):
		brew_command = 'brew outdated'
		macOS_command = 'softwareupdate -l'
		macOS_res = self.run_command(macOS_command)
		brew_res = self.run_command(brew_command)
		return macOS_res, brew_res

	def mac_os_install(self, version):
		get_installer = f"softwareupdate --fetch-full-installer --full-installer-version {version}"
		install = f"sudo softwareupdate -i 'macOS {version} Update-'"
		ret_list = []
		ret_list.append(self.run_command(get_installer))
		ret_list.append(self.run_command(install))
		return ret_list


	def mac_brew_software_update(self, software_update):
		command = f"brew upgrade {software_update}"
		return self.run_command(command)

	def mac_brew_software_updates(self, software_list):
		output_list = []
		for software in software_list:
			output = self.mac_brew_software_update(software)
			output_list.append(output)

		output = ""
		for o in output_list:
			output += o.create_output()
		return output

	def ubuntu_get_updates_list(self):
		command = "sudo apt-get -u upgrade"
		return self.run_command(command)

if __name__ == "__main__":
	A = Agent()
	print(A._ip)
	print(A._platform)
	print(A.run_command("ls -al"))
	print("--")
	print(A.ubuntu_get_updates_list())
	print("-- Release information --")
	print(A.run_command("lsb_release -a"))

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
