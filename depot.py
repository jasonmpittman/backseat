

class DepotItem:
	def __init__(self, command, command_id):
		# self._host = host
		self._command = command
		self._command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None
