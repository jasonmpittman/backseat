'''
This portion deals with the computers that are registered.
'''

class RegistrationHandler:
	def __init__(self):
		self._host_list = []

	def add(self, host, OS):
		self._host_list.append({"host": host, "OS": OS})


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

	def get_centOS_hosts(self):
		return self.get_hosts("CentOS")
		# This may need to be cut into more than 1 pieces

	def get_fedora_hosts(self):
		return self.get_host("Fedora")
