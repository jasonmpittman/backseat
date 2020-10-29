
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
	def __init__(self, host):
		self.host = host
		self.depot_items_list = []
		self.count = 0 # -1 when done = True
		# self._depot_completed_list = []

	def get_by_id(self, id):
		for command_object in self.depot_items_list:
			if command_object.command_id == id:
				return command_object

	def get_next(self):
		for dp in self.depot_items_list:
			if dp._done == False:
				# self.count -= 1
				print(f"get_next: [command]{dp.command}, [command_id]{dp.command_id}, [count]{self.count}")
				return {"command": dp.command, "command_id": dp.command_id, "depot_count": self.count}
		return None

	def add(self, command):
		new_depot_item = DepotItem(command, self.get_depot_list_len()+1)
		self.depot_items_list.append(new_depot_item)
		# print(new_depot_item.output())
		self.count += 1

	def get_depot_list_len(self):
		#This function is for if I decide to change the model to having 2 lists instead of 1
		return len(self.depot_items_list)


	def mass_load_depot(self, command_list):
		for command in command_list:
			self.add(command)

	def print_depot_contents(self):
		for dp_item in self.depot_items_list:
			print(dp_item.output())

	def get_depot_contents(self):
		output = ""
		for dp_item in self.depot_items_list:
			output += dp_item.output() + "\n"
		return output

class DepotList():
	def __init__(self):
		self.list = []

	def add_depot(self, host):
		new_depot = Depot(host)
		self.list.append(new_depot)
		return new_depot

	def get_working_depot(self, host):
		for depot in self.list:
			if depot.host == host:
				return depot

		print("Could not get that depot")
		return None

	def isin(self, host):
		for depot in self.list:
			if host == depot.host:
				return True
		return False

	def add_to_all(self, command):
		for depot in self.list:
			depot.add(command)

	def add_to_specified(self, command, host_list):
		for depot in self.list:
			if depot.host in host_list:
				depot.add(command)

	def print_depot_list(self):
		for depot in self.list:
			print(f"--{depot.host}--")
			depot.print_depot_contents()

	def get_depot_list_info(self):
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
