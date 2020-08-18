'''
This portion deals with the computers that are registered.
'''

class RegistrationHandler:
	def __init__(self):
		self._host_list = []

	def add(self, host, OS):
		self._host_list.append({"host": host, "OS": OS})


	def get_registration_info(self):
		with open("host.config", "r") as F:
			# Add the next portion to this


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
