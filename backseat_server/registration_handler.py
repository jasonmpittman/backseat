'''
This portion deals with the computers that are registered.
'''

from shared import log_handler

class RegistrationHandler:
	def __init__(self):
		'''
		Sets up the hostlist and gets registration information from a file.
		'''
		self._log = log_handler.LogHandler(self.__class__.__name__)
		self._host_list = []
		self.get_registration_info()
		self._log.info(self.__init__.__name__, "_host_list initialized and registration information recieved from host.config file")

	def add(self, FQDN, OS):
		'''
		Adds provided FQDN and OS to the self._host_list.
		'''
		self._host_list.append({"FQDN": FQDN, "OS": OS})
		self._log.info(self.add.__name__, f"Host [{FQDN}] with OS [{OS}] has been added to self._host_list")

	def get_registration_info(self):
		'''
		This function gets all the information from the host file and puts it into self._host_list.
		'''
		with open("../host.config", "r") as F:
			self._log.info(self.get_registration_info.__name__, "host.config successfully opened")
			self._host_list = []
			self._log.info(self.get_registration_info.__name__, "self._host_list set to []")
			lines = F.readlines()
			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				FQDN, OS = line.split(",")
				FQDNs = [h["FQDN"] for h in self._host_list]
				if FQDN not in FQDNs:
					self.add(FQDN, OS)
					self._log.info(self.get_registration_info.__name__, "host added")
				else:
					self._log.warning(self.get_registration_info.__name__, f"repeat host in host.config file: [{FQDN}] is not being added to RegistrationHandler._host_list")

	def write_host_list_to_config(self):
		'''
		Writes all the data in self._host_list into the host.config file (Note: it does not check the contents, it deletes what is in host.config and writes the contents of self._host_list into the file.)
		'''
		with open("../host.config", "w") as F:
			F.write("")
			self._log.info(self.write_host_list_to_config.__name__, "Erased the contents of the host.config file")
			for line in self._host_list:
				F.write(f"{line['FQDN']}, {line['OS']}\n")
			self._log.info(self.write_host_list_to_config.__name__, "Contents of self._host_list put into host.config file")

	def modify_host(self, old_host, new_host, new_OS=""):
		'''
		Gives the ability to change or modify a host, in the event one needs to be edited.
		'''
		self.get_registration_info()
		found = False
		for item in self._host_list:
			if item["FQDN"] == old_host:
				found = True
				item["FQDN"] = new_host
				if new_OS != "":
					item["OS"] = new_OS
				self._log.info(self.modify_host.__name__, "host found and modified")
				break

		if not found:
			self._log.warning(self.modify_host.__name__, "old_host does not match any hosts in the file")
		else:
			self.write_host_list_to_config()


	def delete_host(self, FQDN):
		'''
		Removes a given host from the host.config file (and self._host_list).
		'''
		self.get_registration_info()
		found = False
		for item in self._host_list:
			if item["FQDN"] == FQDN:
				found = True
				self._host_list.remove(item)
				self._log.info(self.delete_host.__name__, f"host [{FQDN}] removed")
				break

		if not found:
			self._log.warning(self.delete_host.__name__, f"delete_host: Host [{FQDN}] not found, nothing deleted")
		else:
			self.write_host_list_to_config()

	def register_new_host(self, new_FQDN, new_OS):
		'''
		Adds a provided new, unique host to the host.config file.
		'''
		current_hosts = []
		with open("../host.config", "r") as F:
			lines = F.readlines()
			for line in lines:
				line = line.replace("\n", "")
				line = line.replace(" ", "")
				FQDN, OS = line.split(",")
				current_hosts.append(FQDN)

		with open("../host.config", "a") as F:
			# F.write(f"{host}, {OS}\n")
			self._log.info(self.register_new_host.__name__, "Checking if host is unique")
			if new_FQDN not in current_hosts:
				F.write(f"{new_FQDN}, {new_OS}\n")
				self._log.info(self.register_new_host.__name__, "Host addded")
			else:
				self._log.info(self.register_new_host.__name__, f"Host is already in host.config file: [{new_FQDN}, {new_OS}]")

	def get_hosts(self, host_type):
		'''
		Returns a list of hosts for a given OS.
		'''
		res = []
		for host in self._host_list:
			if host["OS"] == host_type:
				res.append(host)
		self._log.info(self.get_hosts.__name__, f"Returning a list of hosts with OS [{host_type}]")
		return res

	def get_mac_hosts(self):
		'''
		Returns MacOS Hosts
		'''
		return self.get_hosts("MacOS")

	def get_ubuntu_hosts(self):
		'''
		Returns Ubuntu Hosts
		'''
		return self.get_hosts("Ubuntu")

	def get_centOS_7_hosts(self):
		'''
		Returns CentOS7 Hosts
		'''
		return self.get_hosts("CentOS7")

	def get_centOS_8_hosts(self):
		'''
		Returns CentOS8 Hosts
		'''
		return self.get_hosts("CentOS8")

	def get_fedora_hosts(self):
		'''
		Returns Fedora Hosts
		'''
		return self.get_host("Fedora")

	def print_host_list(self):
		'''
		Prints the contents of self._host_list.
		'''
		self.get_registration_info()
		for host in self._host_list:
			print(f"{host['FQDN']}: {host['OS']}")

if __name__ == "__main__":
	RH = RegistrationHandler()
	RH.print_host_list()
	print("--")
	RH.delete_host("")
	RH.print_host_list()
