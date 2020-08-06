

class DepotItem:
	def __init__(self, command, command_id):
		# self._host = host
		self._command = command
		self.command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None

	def set(self, done, stdout, exit_code):
		self._done = done
		self._stdout = stdout
		self._exit_code = exit_code

	def output(self):
		return f"{self._command}, {self.command_id}, {self._done}, {self._stdout}, {self._exit_code}"

class Depot:
	def __init__(self, host):
		self.host = host
		self._depot_active_list = []
		self.count = 0
		# self._depot_completed_list = []

	def get_by_id(self, id):
		for command_object in self._depot_active_list:
			if command_object.command_id == id:
				return command_object

	def get_next(self):
		for dp in self._depot_active_list:
			if dp._done == False:
				self.count -= 1
				return dp._command, dp._command_id, self.count
		return None

	def add(self, command, command_id):
		new_depot_item = DepotItem(command, command_id)
		self._depot_active_list.append(new_depot_item)
		self.count += 1
