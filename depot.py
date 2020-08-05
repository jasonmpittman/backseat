

class DepotItem:
	def __init__(self, command, command_id):
		# self._host = host
		self._command = command
		self.command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None

class Depot:
	def __init__(self, host):
		self.host = host
		self._depot_active_list = []
		# self._depot_completed_list = []

	def get_by_id(self, id):
		for command_object in self._depot_active_list:
			if command_object.command_id == id:
				return command_object
