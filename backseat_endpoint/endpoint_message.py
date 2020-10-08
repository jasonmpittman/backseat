import json

class EndpointMessage:
	"""
	This class creates the json that is used to be sent to the server.

	Attributes
	----------
	_ping : bool
	_ready : bool
	_completed : bool
	_stdout : str
	_stderr : str
	_successful : bool
	_exit_code : int
	_command_id : int
	"""
	def __init__(self):
		pass

	def create_msg(self, ping, ready, completed, stdout, stderr, successful, exit_code, command_id):
		"""
		This function creates the message and returns the json.

		Parameters
		----------
		ping : bool
		ready : bool
		completed : bool
		stdout : str
		stderr : str
		successful : bool
		exit_code : int
		command_id : int
		"""
		self.add_data(ping, ready, completed, stdout, stderr, successful, exit_code, command_id)
		return self.to_json()

	def add_data(self, ping, ready, completed, stdout, stderr, successful, exit_code, command_id):

		"""
		This function fills the class member variables with the provided value.

		Parameters
		----------
		ping : bool
		ready : bool
		completed : bool
		stdout : str
		stderr : str
		successful : bool
		exit_code : int
		command_id : int
		"""

		self._ping = ping
		self._ready = ready
		self._completed = completed
		self._stdout = stdout
		self._stderr = stderr
		self._successful = successful
		self._exit_code = exit_code
		self._command_id = command_id

	def to_json(self):
		"""
		Converts what is in the member variables into json.

		Parameters
		----------
		"""
		dict = {"ping": self._ping, "ready": self._ready, "completed": self._completed, "stdout": self._stdout, "stderr": self._stderr, "successful": self._successful, "exit_code": self._exit_code, "command_id": self._command_id}
		output_json = json.dumps(dict)

		return output_json

	def get_ping_msg(self):
		"""
		Creates a message that can be used to ping the server to see if any
		commands are in the depot.
		
		Parameters
		----------
		"""
		return self.create_msg(True, True, True, "", "", False, -1, 0)

if __name__ == "__main__":
	m = ClientMessage()
	m.add_data("localhost",True, True, "woo\nwoon\nToon\n---", "", True, 1)
	output = m.to_json()
	print(output)
