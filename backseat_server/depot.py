
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
	"""
	def __init__(self, command, command_id):
		"""
		This initializes the creation of a depot item.

		Parameters
		----------
		command : str
		command_id : int
		"""
		self.command = command
		self.command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None

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

	def output(self):
		"""
		This function returns all the attributes of a DepotItem as a string.
		"""
		return f"Command:{self.command}\n Command ID: {self.command_id}\n Done: {self._done}\n stdout: {self._stdout}\n Exit Code: {self._exit_code}\n"

class Depot:
	"""
	Depot objects hold all of the commands that a given endpoint is to or has run.

	Attributes
	----------
	host : str
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
		# self._depot_completed_list = []

	def get_by_id(self, id):
		"""
		This function returns a depot item by the unique command_id.

		Parameters
		----------
		id : str
		"""
		for command_object in self.depot_items_list:
			if command_object.command_id == id:
				return command_object

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
				return {"command": dp.command, "command_id": dp.command_id, "depot_count": self.count}
		return None

	def add(self, command):
		"""
		Creates a new depot item for the provided command.

		Parameters
		----------
		command : str
		"""
		new_depot_item = DepotItem(command, self.get_depot_list_len()+1)
		self.depot_items_list.append(new_depot_item)
		# print(new_depot_item.output())
		self.count += 1

	def get_depot_list_len(self):
		"""
		Returns the length of the list of depot items.

		Parameters
		----------
		"""
		return len(self.depot_items_list)



	def mass_load_depot(self, command_list):
		"""
		This adds the provided list of commands to the depot, in order all at one time. If you wanted to add a batch of commands to a depot, use this function.

		Parameters
		----------
		command_list : list of str
		"""
		for command in command_list:
			self.add(command)

	def print_depot_contents(self):
		"""
		Prints the contents of the depot.

		Parameters
		----------
		"""
		for dp_item in self.depot_items_list:
			print(dp_item.output())

	def get_depot_contents(self):
		"""
		Returns the contents of the depot as a str.

		Parameters
		----------
		"""
		output = ""
		for dp_item in self.depot_items_list:
			output += dp_item.output() + "\n"
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
		self.list = []

	def add_depot(self, host):
		"""
		Adds a depot to the list then returns the newly created depot.

		Parameters
		----------
		host : str
		"""
		new_depot = Depot(host)
		self.list.append(new_depot)
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
				return depot

		print("Could not get that depot")
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
				return True
		return False

	def add_to_all(self, command):
		"""
		Adds the provided command to all depots in the list.

		Parameters
		----------
		command : str
		"""
		for depot in self.list:
			depot.add(command)

	def add_to_specified(self, command, host_list):
		"""
		Adds the provided command to the specified list of depots via host.

		Parameters
		----------
		command : str
		host_list : str
		"""
		for depot in self.list:
			if depot.host in host_list:
				depot.add(command)

	def print_depot_list(self):
		"""
		Prints the contents of the depot_list.

		Parameters
		----------
		"""
		for depot in self.list:
			print(f"--{depot.host}--")
			depot.print_depot_contents()

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
		return o_string

if __name__ == "__main__":
	dl = DepotList()
	dl.add_depot("localhost")
	working_depot = dl.get_working_depot("localhost")
	working_depot.mass_load_depot(["ls -al", "PWD"])

#
