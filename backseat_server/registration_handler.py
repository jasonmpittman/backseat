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
		with open("host.config", "r") as F:
			# Add the next portion to this
			lines = F.readlines()
			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				host, OS = line.split(",")
				hosts = [h["host"] for h in self._host_list]
				if host not in hosts:
					self.add(host, OS)
				else:
					print(f"repeat host [{host}] is not being added to self._host_list")

	def register_new_host(self, host, OS):
		current_hosts = []
		with open("host.config", "r") as F:
			lines = F.readlines()
			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				host, OS = line.split(",")
				current_hosts.append(host)

		with open("host.config", "a") as F:
			F.write(f"{host}, {OS}\n")


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
		return self.get_hosts("CentOS 7")

	def get_centOS_8_hosts(self):
		return self.get_hosts("CentOS 8")

	def get_fedora_hosts(self):
		return self.get_host("Fedora")

	def print_host_list(self):
		for host in self._host_list:
			print(f"{host['host']}: {host['OS']}")




if __name__ == "__main__":
	RH = RegistrationHandler()
	RH.print_host_list()
	RH.register_new_host("132.456.789.1011", "Ubuntu")
