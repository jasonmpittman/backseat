import json

class EndpointMessage:
	def __init__(self):
		pass

	def create_msg(self, ping, ready, completed, stdout, stderr, successful, exit_code, command_id):
		self.add_data(ping, ready, completed, stdout, stderr, successful, exit_code, command_id)
		return self.to_json()

	def add_data(self, ping, ready, completed, stdout, stderr, successful, exit_code, command_id):
		self._ping = ping
		self._ready = ready
		self._completed = completed
		self._stdout = stdout
		self._stderr = stderr
		self._successful = successful
		self._exit_code = exit_code
		self._command_id = command_id

	def to_json(self):
		dict = {"ping": self._ping, "ready": self._ready, "completed": self._completed, "stdout": self._stdout, "stderr": self._stderr, "successful": self._successful, "exit_code": self._exit_code, "command_id": self._command_id}
		print("-----Dict----")
		print(type(dict))
		output_json = json.dumps(dict)
		print(output_json)
		return output_json

	def get_ping_msg(self):
		return self.create_msg(True, True, True, "", "", False, -1, 0)

if __name__ == "__main__":
	m = ClientMessage()
	m.add_data("localhost",True, True, "woo\nwoon\nToon\n---", "", True, 1)
	output = m.to_json()
	print(output)
