'''
This portion deals with the computers that are registered.
'''

from shared import log_handler

from shared import asym_cryptography_handler as crypto

# Name OS Public_Key
class RegistrationHandler:
	def __init__(self):
		"""
		Sets up the hostlist and gets registration information from a file.

		Attributes
		----------
		host_list : python list
		crypto_handler : AsymmetricCryptographyHandler object
		"""
		self._log = log_handler.LogHandler(self.__class__.__name__)
		self.host_list = []
		self.get_registration_info()
		self._log.info(self.__init__.__name__, "_host_list initialized and registration information recieved from host.config file")
		self.crypto_handler = crypto.AsymmetricCryptographyHandler()

	def get_by_name(self, name):
		"""
		This function gets the host information about an endpoint by name. Returns that data if it finds it and returns None if it fails to find it.

		Parameters
		----------
		name : str
		"""
		for host in self.host_list:
			if host["name"] == name:
				return host
		return None

	def get_registration_info(self):
		"""
		This function gets all the information from the host file and puts it into self.host_list.

		Parameters
		----------
		"""
		with open("host.config", "r") as F:
			self._log.info(self.get_registration_info.__name__, "host.config successfully opened")
			self.host_list = []
			self._log.info(self.get_registration_info.__name__, "self.host_list set to []")
			lines = F.readlines()

			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				name, OS, public_key, ip, port = line.split(",")
				names = [h["name"] for h in self.host_list]

				if name not in names:
					self.add(name, OS, public_key, ip, port)
					self._log.info(self.get_registration_info.__name__, "host added")
				else:
					self._log.warning(self.get_registration_info.__name__, f"repeat host in host.config file: [{name}] is not being added to RegistrationHandler._host_list")


	def add(self, name, OS, public_key, ip, port):
		"""
		Adds name, OS, and public_key to the host_list

		Parameters
		----------
		name : str
		OS : str
		public_key : str
		ip : str
		port : int
		"""
		self._log.info("add", f"Host: {name} added to host_list")
		self.host_list.append({"name": name, "OS": OS, "public_key": public_key, "ip": ip, "port": port})

	def get_hosts(self, host_type):
		"""
		Returns a list of hosts for a given OS.

		Parameters
		----------
		host_type : str
		"""
		res = []
		for host in self.host_list:
			if host["OS"] == host_type:
				res.append(host)
		self._log.info(self.get_hosts.__name__, f"Returning a list of hosts with OS [{host_type}]")
		return res

	def get_mac_hosts(self):
		"""
		Returns MacOS Hosts

		Parameters
		----------
		"""
		return self.get_hosts("MacOS")

	def get_ubuntu_hosts(self):
		"""
		Returns Ubuntu Hosts

		Parameters
		----------
		"""
		return self.get_hosts("Ubuntu")

	def get_centOS_7_hosts(self):
		"""
		Returns CentOS7 Hosts

		Parameters
		----------
		"""
		return self.get_hosts("CentOS7")

	def get_centOS_8_hosts(self):
		"""
		Returns CentOS8 Hosts

		Parameters
		----------
		"""
		return self.get_hosts("CentOS8")

	def get_fedora_hosts(self):
		"""
		Returns Fedora Hosts

		Parameters
		----------
		"""
		return self.get_hosts("Fedora")

	def print_host_list(self):
		"""
		Prints the contents of self.host_list.

		Parameters
		----------
		"""
		self.get_registration_info()
		for host in self.host_list:
			print(f"{host['name']}: {host['OS']}")

