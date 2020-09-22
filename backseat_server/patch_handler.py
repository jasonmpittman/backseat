'''
Handles everything involved with patches, gets them, and creates installation commands.
'''

class PatchHandler:
	def __init__(self, depot_list=None):
		if depot_list == None:
			print("depot_list == None")



	def mac_get_updates_list(self):
		return 'brew outdated'


	def macOS_get_update(self):
		return 'softwareupdate -l'


	# def mac_os_install(self, version):
	# 	get_installer = f"softwareupdate --fetch-full-installer --full-installer-version {version}"
	# 	install = f"sudo softwareupdate -i 'macOS {version} Update-'"
	# 	ret_list = []
	# 	ret_list.append(self.run_command(get_installer))
	# 	ret_list.append(self.run_command(install))
	# 	return ret_list


	def mac_brew_software_update(self, software_update):
		return f"brew upgrade {software_update}"

	# def mac_brew_software_updates(self, software_list):
	# 	output_list = []
	# 	for software in software_list:
	# 		output = self.mac_brew_software_update(software)
	# 		output_list.append(output)
	#
	# 	output = ""
	# 	for o in output_list:
	# 		output += o.create_output()
	# 	return output

	def ubuntu_get_updates_list(self):
		return "apt list --upgradable"

	def ubuntu_run_package_update(self, package):
		return f"apt-get upgrade {package}"

	def ubuntu_check_os_update(self):
		return "do-release-upgrade -c"

	def ubuntu_run_os_update(self):
		return "sudo do-release-upgrade"

#Redhat
#works for Fedora7 and CentOS7
	def yum_list_updates(self):
		return "yum check-update"

	def yum_update_all_packages(self):
		return "yum update"

	def yum_update_package(self, package):
		return f"yum update {package}"

#works for Fedora8 and CentOS8
	def dnf_list_updates(self):
		return "dnf check-update"

	def dnf_update_all_packages(self):
		return "dnf upgrade"

	def dnf_install_package(self, package):
		return f"dnf install {package}"



if __name__ == "__main__":
	PH = PatchHandler()
