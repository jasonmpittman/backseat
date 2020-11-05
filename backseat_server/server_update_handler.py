from shared import tcp_socket_handler

from shared import log_handler

from shared import read_server_config

class ServerUpdateHandler:
	def __init__(self):
		ip, port, server_private_key, server_public_key = read_server_config.get_server_config()

		self._socket_handler = tcp_socket_handler.TcpSocketHandler(server_private_key, serer_public_key)

	def _message_maker(self):
		pass

	def add_command(self, command, endpoint_list):
		pass

	def override_command(self, command_id):
		pass

	def get_info(self):
		pass
