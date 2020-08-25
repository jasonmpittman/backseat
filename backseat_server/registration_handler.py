'''
This portion deals with the computers that are registered.
'''

class RegistrationHandler:
	def __init__(self):
		self._host_list = []
		self.get_registration_info()

	def add(self, host, OS):
		self._host_list.append({"host": host, "OS": OS})

	def get_registration_info(self):
		with open("../host.config", "r") as F:
			self._host_list = []
			lines = F.readlines()
			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				host, OS = line.split(",")
				hosts = [h["host"] for h in self._host_list]
				if host not in hosts:
					self.add(host, OS)
				else:
					print(f"repeat host in host.config file: [{host}] is not being added to RegistrationHandler._host_list")

	def write_host_list_to_config(self):
		with open("../host.config", "w") as F:
			F.write("")
			for line in self._host_list:
				F.write(f"{line['host']}, {line['OS']}\n")

	def modify_host(self, old_host, old_OS, new_host, new_OS):
		self.get_registration_info()
		found = False
		for item in self._host_list:
			if item["host"] == old_host and item["OS"] == old_OS:
				found = True
				item["host"] = new_host
				item["OS"] = new_OS
		if not found:
			print("old_host and old_OS do not match any hosts in the file")
		else:
			print("hostlist:")
			print(self._host_list)
			self.write_host_list_to_config()


	def delete_host(self, host):
		self.get_registration_info()
		found = False
		for item in self._host_list:
			if item["host"] == host:
				found = True
				self._host_list.remove(item)

		if not found:
			print(f"delete_host: Host [{host}] not found, nothing deleted")
		else:
			self.write_host_list_to_config()


	def register_new_host(self, host, OS):
		current_hosts = []
		with open("../host.config", "r") as F:
			lines = F.readlines()
			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				host, OS = line.split(",")
				current_hosts.append(host)

		with open("../host.config", "a") as F:
			# F.write(f"{host}, {OS}\n")
			if host not in current_hosts:
				F.write(f"{host}, {OS}\n")
			else:
				print(f"Host is already in host.config file: [{host}, {OS}]")

	def get_hosts(self, host_type):
		res = []
		for host in self._host_list:
			if host["OS"] == host_type:
				res.append(host)
		return res

	def get_mac_hosts(self):
		return self.get_hosts("MacOS")

	def get_ubuntu_hosts(self):
		return self.get_hosts("Ubuntu")

	def get_centOS_7_hosts(self):
		return self.get_hosts("CentOS7")

	def get_centOS_8_hosts(self):
		return self.get_hosts("CentOS8")

	def get_fedora_hosts(self):
		return self.get_host("Fedora")

	def print_host_list(self):
		self.get_registration_info()
		for host in self._host_list:
			print(f"{host['host']}: {host['OS']}")

if __name__ == "__main__":
	RH = RegistrationHandler()
	RH.print_host_list()
	print("--")
	RH.delete_host("444.333.222.111")
	RH.print_host_list()
