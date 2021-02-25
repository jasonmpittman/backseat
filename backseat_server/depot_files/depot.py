from shared import log_handler

from backseat_server.depot_files import depot_item

class Depot:
	"""
	Depot objects hold all of the commands that a given endpoint is to or has run.

	Attributes
	----------
	host : str
	depot_items_list : python list
	count : int
	"""
	def __init__(self, host, name):
		"""
		Creates a depot for a provided host.

		Parameters
		----------
		host : str
		name : str
		"""
		self.host = host
		self.name = name
		self.depot_items_list = []
		self.count = 0 # -1 when done = True
		self._log = log_handler.LogHandler("Depot")
		self._log.info("__init__", f"Depot for {host} initialized")

	def get_by_id(self, id):
		"""
		This function returns a depot item by the unique command_id.

		Parameters
		----------
		id : int
		"""
		for command_object in self.depot_items_list:
			if command_object.command_id == id:
				self._log.info("get_by_id", f"Returned DepotItem with command_id: {id}")
				return command_object

		self._log.error("get_by_id", "Item could not be found, returned None")
		return None
		# HANDLE THIS CASE

	def get_next(self):
		"""
		Returns the next uncompleted depot item.

		Parameters
		----------
		"""
		for dp in self.depot_items_list:
			if dp._done == False:
				# self.count -= 1
				print(f"get_next: [command]{dp.command}, [command_id]{dp.command_id}, [count]{self.count}")

				self._log.info("get_next", f"Next item found Returned DepotItem with command_id: {dp.command_id}")

				return {"command": dp.command, "command_id": dp.command_id, "depot_count": self.count}

		self._log.warning("get_next", "No next item can be found, returned None")
		return None

	def add(self, command, item_order):
		"""
		Creates a new depot item for the provided command.

		Parameters
		----------
		command : str
		item_iterator : str
		"""
		new_depot_item = depot_item.DepotItem(command, self.get_depot_list_len()+1, item_order)
		self.depot_items_list.append(new_depot_item)
		# print(new_depot_item.output())
		self.count += 1
		self._log.info("add", f"command: {command} added")

	def get_depot_list_len(self):
		"""
		Returns the length of the list of depot items.

		Parameters
		----------
		"""
		length = len(self.depot_items_list)
		self._log.info("get_depot_list_len", f"Returned {length}")
		return length

	def print_depot_contents(self):
		"""
		Prints the contents of the depot.

		Parameters
		----------
		"""
		for dp_item in self.depot_items_list:
			print(dp_item.output())
		self._log.info("print_depot_contents", f"Printed contents of depot {self.host}")

	def get_depot_contents(self):
		"""
		Returns the contents of the depot as a str.

		Parameters
		----------
		"""
		output = ""
		for dp_item in self.depot_items_list:
			output += dp_item.output() + "\n"
		self._log.info("get_depot_contents", f"Returned depot contents for depot {self.host}")
		return output