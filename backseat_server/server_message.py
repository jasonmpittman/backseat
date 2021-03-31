import json

class ServerMessage:
	"""
	Creates the messages that the server sends to the endpoints.

	Attributes
	----------
	_not_ready : bool
	_command : str
	_sudo : bool
	_password : str
	_sequence : int
	_depot_items : int
	_command_id : int
	"""

	def create_msg(self, not_ready, command, sudo, password, sequence, depot_items, command_id):
		"""
		Sets the values of the variables that belong to the class then returns that information in json format.

		Parameters
		----------
		not_ready : bool
		command : str
		sudo : bool
		password : str
		sequence : int
		depot_items : int
		command_id : int
		"""
		self.add_data(not_ready, command, sudo, password, sequence, depot_items, command_id)
		return self.to_json()

	def add_data(self, not_ready, command, sudo, password, sequence, depot_items, command_id=0):
		"""
		Sets the values of the variables that belong to the class.

		Parameters
		----------
		not_ready : bool
		command : str
		sudo : bool
		password : str
		sequence : int
		depot_items : int
		command_id : int
		"""
		self._not_ready = not_ready
		self._command = command
		self._sudo = sudo
		self._password = password
		self._sequence = sequence
		self._depot_items = depot_items
		self._command_id = command_id

	def to_json(self):
		"""
		Converts the variables that belong to the class into json format then return the json str.

		Parameters
		----------
		"""
		res_dict = {"not_ready": self._not_ready, "command": self._command, "sudo": self._sudo, "password": self._password, "sequence": 0, "depot_items": self._depot_items, "command_id": self._command_id}
		output_json = json.dumps(res_dict)
		return output_json

