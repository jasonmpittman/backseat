
#Needs better system to keep track of # of items in depot
class DepotItem:
	def __init__(self, command, command_id):
		# self._host = host
		self.command = command
		self.command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None

	def set(self, done, stdout, exit_code):
		self._done = done
		self._stdout = stdout
		self._exit_code = exit_code

	def output(self):
		return f"{self.command}, {self.command_id}, {self._done}, {self._stdout}, {self._exit_code}"

class Depot:
	def __init__(self, host):
		self.host = host
		self._depot_items_list = []
		self.count = 0
		# self._depot_completed_list = []

	def get_by_id(self, id):
		for command_object in self._depot_items_list:
			if command_object.command_id == id:
				return command_object

	def get_next(self):
		print(self._depot_items_list)
		for dp in self._depot_items_list:
			print(dp._done)
			if dp._done == False:
				self.count -= 1
				print(f"{dp.command}, {dp.command_id}, {self.count}")
				return (dp.command, dp.command_id, self.count)
		return None

	def add(self, command):
		new_depot_item = DepotItem(command, self.get_depot_list_len()+1)
		self._depot_items_list.append(new_depot_item)
		print(new_depot_item.output())
		self.count += 1

	def get_depot_list_len(self):
		#This function is for if I decide to change the model to having 2 lists instead of 1
		return len(self._depot_items_list)


	def mass_load_depot(self, command_list):
		for command in command_list:
			self.add(command)

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

		return self.add_depot(host)

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

if __name__ == "__main__":
	dp = Depot("localhost")
	dp.mass_load_depot(["ls -al", "PWD"])


#
