from shared import tcp_socket_handler

from shared import log_handler

from shared import read_server_config

import json

# message_dict = {"type": "add", "command": "PWD", "who": ["client1_public.pem"]}
# message_dict = {"type": "checkoff", "command_id": 3, "who": "client1_public.pem"}

# message_dict = {"type": "get_server_data"}

class ServerUpdateHandler:
	def __init__(self):
		self._ip, self._port, self._server_private_key, self._server_public_key = read_server_config.get_server_config()

		self._socket_handler = tcp_socket_handler.TcpSocketHandler(self._server_private_key, self._server_public_key)


	def add_command_message(self, command, endpoint_list):
		msg_dict = {"type": "add", "command": command, "who": endpoint_list}
		message = json.dumps(msg_dict)
		self.send_server_update(message)



	def override_command_message(self, command_id, who):
		msg_dict = {"type": "checkoff", "command_id": command_id, "who": who}
		message = json.dumps(msg_dict)
		self.send_server_update(message)

	def get_info_message(self):
		msg_dict = {"type": "get_server_data"}
		message = json.dumps(msg_dict)
		self.send_server_update(message)
		data = recieve_server_info()

	def send_server_update(self, message):
		client_conn = self._socket_handler.create_client_socket_connect(self._ip, self._port)
		self._socket_handler.send(client_conn, message, self._server_public_key)

	def recieve_server_info(self):
		pass
