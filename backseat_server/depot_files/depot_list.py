from shared import log_handler

from backseat_server.depot_files import depot_item

from backseat_server.depot_files import depot

class DepotList():
	"""
	This class holds and manages all of the depots.

	Attributes
	----------
	list : list of depot objects
	"""
	def __init__(self):
		"""
		Initializes the list that holds the depot objects.

		Parameters
		----------
		"""
		self._log = log_handler.LogHandler("DepotList")
		self.list = []
		self._log.info("__init__", "DepotList Initialized")
		self._item_order = 1

	def add_depot(self, host, name):
		"""
		Adds a depot to the list then returns the newly created depot.

		Parameters
		----------
		host : str
		"""
		new_depot = depot.Depot(host, name)
		self.list.append(new_depot)
		self._log.info("add_depot", f"New depot added for {host}")
		return new_depot

	def get_working_depot(self, host):
		"""
		Provided with a host, this function will find and return the associated depot.

		Parameters
		----------
		host : str
		"""
		for depot in self.list:
			if depot.host == host:
				self._log.info("get_working_depot", f"Depot {host} found and returned")
				return depot

		print(f"Could not find {host} depot")
		self._log.warning("get_working_depot", f"Could not find {host} depot, Returned None")

		return None

	def isin(self, host):
		"""
		Determines if a provided host has a depot associated with it in the depot_list.

		Parameters
		----------
		host : str
		"""
		for depot in self.list:
			if host == depot.host:
				self._log.info("isin", f"Host {host} has a depot associated with it in the depot_list")
				return True
		self._log.info("isin", f"Host {host} does not have a depot associated with it")
		return False

	def add_to_all(self, command):
		"""
		Adds the provided command to all depots in the list.

		Parameters
		----------
		command : str
		"""
		self._log.info("add_to_all", f"Adding command [{command}] to all depots")
		for depot in self.list:
			depot.add(command, self._item_order)
			self._item_order += 1

	def add_to_specified(self, command, host_list):
		"""
		Adds the provided command to the specified list of depots via host.

		Parameters
		----------
		command : str
		host_list : str
		"""
		print("add_to_specified ran")
		print(f"host: {host_list}, command = {command}")
		print(self.list)
		self._log.info("add_to_specified", "Adding command to specified depots")
		for depot in self.list:
			if depot.host in host_list:
				depot.add(command, self._item_order)
				self._item_order += 1

	def print_depot_list(self):
		"""
		Prints the contents of the depot_list.

		Parameters
		----------
		"""
		for depot in self.list:
			print(f"--{depot.host}--")
			depot.print_depot_contents()
		self._log.info("print_depot_list", "Printed depot list")

	def get_depot_list_info(self):
		"""
		Creates a depot list output string, then returns it.

		Parameters
		----------
		"""
		o_string = ""
		for depot in self.list:
			o_string += f"--{depot.host}--\n"
			o_string += depot.get_depot_contents() + "\n"

		self._log.info("get_depot_list_info", "Returned depot list info in string format")

		return o_string
