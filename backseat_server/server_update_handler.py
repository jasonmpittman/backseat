from shared import tcp_socket_handler

from shared import log_handler

from shared import read_server_config

import json

import time

# message_dict = {"type": "add", "command": "PWD", "who": ["client1_public.pem"]}
# message_dict = {"type": "checkoff", "command_id": 3, "who": "client1_public.pem"}

# message_dict = {"type": "get_server_data"}

class ServerUpdateHandler:
	def __init__(self):
		self._ip, self._port, self._server_private_key, self._server_public_key = read_server_config.get_server_config()

		self._socket_handler = tcp_socket_handler.TcpSocketHandler(self._server_private_key, self._server_public_key)
		self._client_conn = None

	def add_command(self, command, endpoint_list):
		msg_dict = {"type": "add", "command": command, "who": endpoint_list}
		message = json.dumps(msg_dict)
		self._send_server_update(message)

	def override_command(self, command_id, who):
		msg_dict = {"type": "checkoff", "command_id": command_id, "who": who}
		message = json.dumps(msg_dict)
		self._send_server_update(message)

	def get_info_message(self):
		msg_dict = {"type": "get_server_data"}
		message = json.dumps(msg_dict)
		self._send_server_update(message)
		return self._recieve_server_info()

	def print_info_message(self, info_message):
		print("--Server Status--")
		print(f"Start Time: {self._date_time_format(info_message['start_time'])}")

		print(f"Run Time: {self._elapsed_time_format(info_message['run_time'])}")

		print(f"Time Since Last Successful Job: {self._elapsed_time_format(info_message['last_successful_job_time'])}")
		print(f"Last successful job: {info_message['last_successful_job']}")
		print(f"Last Heartbeat_time: {self._date_time_format(info_message['last_heartbeat_time'])}")
		print(f"Time since heartbeat: {self._elapsed_time_format(info_message['time_since_heartbeat'])}")
		print("--Depots' Info--")





	def _send_server_update(self, message):
		self._client_conn = self._socket_handler.create_client_socket_connect(self._ip, self._port)
		self._socket_handler.send(self._client_conn, message, self._server_public_key)

	def _recieve_server_info(self):
		data, _ = self._socket_handler.recieve(self._client_conn)
		print(data)
		# return data_dict
		data = json.loads(data)
		return data


	def _date_time_format(self, the_time):
		return time.strftime("%a, %b %d, %Y %I:%M:%S %p", time.localtime(the_time))

	def _elapsed_time_format(self, elapsed_time):
		# return time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
		# e = int(time.gmtime(elapsed_time))
		# return f"{e // 3600}:{(e % 3600 // 60)}:{e % 60}"
