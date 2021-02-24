from shared import log_handler

class DepotItem:
	"""
	This class keeps track of individual commands, the command id, if the command has been run, the output of the command, and the exit code. These items are put into depots which keep track of which endpoint it belongs to.

	Attributes
	----------
	command : str
	command_id : int
	_done : bool
	_stdout : str
	_exit_code : int
	_item_order : int
	"""
	def __init__(self, command, command_id, item_order):
		"""
		This initializes the creation of a depot item.

		Parameters
		----------
		command : str
		command_id : int
		item_iterator : int
		"""
		self._log = log_handler.LogHandler("DepotItem")
		self.command = command
		self.command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None
		self._log.info("__init__", f"DepotItem created: {command} {command_id}")
		self._item_order = item_order

	def set(self, done, stdout, exit_code):
		"""
		This function sets the values for a command that has already ran.

		Parameters
		----------
		done : bool
		stdout : str
		exit_code : int
		"""
		self._done = done
		self._stdout = stdout
		self._exit_code = exit_code
		self._log.info("set", f"Item with command_id={self.command_id}, values set. done={done} stdout={stdout} exit_code={exit_code}")

	def output(self):
		"""
		This function returns all the attributes of a DepotItem as a string.

		Parameters
		----------
		"""
		self._log.info("output", f"Returning DepotItem with command_id [{self.command_id}] values as a string")
		return f"Command:{self.command}\n Command ID: {self.command_id}\n Done: {self._done}\n stdout: {self._stdout}\n Exit Code: {self._exit_code}\n item_iterator: {self._item_order}\n"

	def get_info(self):
		return {"command": self.command, "command_id": self.command_id, "done": self._done, "stdout": self._stdout, "exit_code": self._exit_code, "item_iterator": self._item_order}

class Depot:
	"""
	Depot objects hold all of the commands that a given endpoint is to or has run.

	Attributes
	----------
	host : str
	depot_items_list : python list
	count : int
	"""
	def __init__(self, host):
		"""
		Creates a depot for a provided host.

		Parameters
		----------
		host : str
		"""
		self.host = host
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
		new_depot_item = DepotItem(command, self.get_depot_list_len()+1, item_order)
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

	def add_depot(self, host):
		"""
		Adds a depot to the list then returns the newly created depot.

		Parameters
		----------
		host : str
		"""
		new_depot = Depot(host)
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

if __name__ == "__main__":
	dl = DepotList()
	dl.add_depot("localhost")
	working_depot = dl.get_working_depot("localhost")

#
