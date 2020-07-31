import json

class ServerMessage:
	def __init__(self):
		pass

	def add_data(self, command, sudo, password, sequence, depot_items):
		self._command = command
		self._sudo = sudo
		self._password = password
		self._sequence = sequence
		self._depot_items = depot_items

	def to_json(self):
		dict = {"command": self._command, "sudo": self._sudo, "password": self._password, "sequence": 0, "depot_items": self._depot_items}
		output_json = json.dumps(dict)
		return output_json

if __name__ == "__main__":
	m = ServerMessage()
	m.add_data("ls -al", False, "", 0, 1)
	output = m.to_json()
	print(output)
