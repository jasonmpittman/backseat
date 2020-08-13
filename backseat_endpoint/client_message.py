import json

class ClientMessage:
	def __init__(self):
		pass

	def add_data(self, whoami, ping, ready, completed, stdout, stderr, successful, exit_code, command_id):
		self._whoami = whoami
		self._ping = ping
		self._ready = ready
		self._completed = completed
		self._stdout = stdout
		self._stderr = stderr
		self._successful = successful
		self._exit_code = exit_code
		self._command_id = command_id

	def to_json(self):
		dict = {"whoami": self._whoami, "ping": self._ping, "ready": self._ready, "completed": self._completed, "stdout": self._stdout, "stderr": self._stderr, "successful": self._successful, "exit_code": self._exit_code, "command_id": self._command_id}
		output_json = json.dumps(dict)
		return output_json

if __name__ == "__main__":
	m = ClientMessage()
	m.add_data("localhost",True, True, "woo\nwoon\nToon\n---", "", True, 1)
	output = m.to_json()
	print(output)
