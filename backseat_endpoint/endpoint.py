from backseat_endpoint import agent

from shared import tcp_socket_handler

from backseat_endpoint import endpoint_message

import json

class Endpoint:
	def __init__(self, serv_ip, serv_port, private_key, server_public_key):
		self._agent = agent.Agent()
		self._tcp_socket_handler = tcp_socket_handler.TcpSocketHandler()
		self._ip = serv_ip
		self._port = serv_port
		self._client = None
		#Add something to the config file to deal with these
		self._my_private_key = private_key
		self._server_public_key = server_public_key
		self._endpoint_msg = endpoint_message.EndpointMessage()


	def connect(self):
		self._client = self._tcp_socket_handler.create_client_socket_connect(self._ip, self._port)

	def get_command_msg(self):
		try:
			self.connect()
		except:
			pass
		message = self._endpoint_msg.get_ping_msg()
		print("Message being sent:")
		print(message)
		print("---")
		self._tcp_socket_handler.send(self._client, message, self._server_public_key, self._my_private_key)
		print("---")
		responce, sender_key = self._tcp_socket_handler.recieve(self._client, self._my_private_key)
		print("--")
		print(responce)
		print("--")
		if responce == None:
			print("responce = None")
		else:
			json_responce = json.loads(responce)
		return json_responce

	def run_command(self, command_msg_json):

		stdout, exitcode = self._agent.run_command(command_msg_json["command"])
		responce_msg_json = self._endpoint_msg.create_msg(False, True, True, stdout, "", True, exitcode, command_msg_json["command_id"])

		return responce_msg_json

	def send_command_res(self, responce_msg_json):
		if responce_msg_json == None:
			print("responce_msg_json = None")
		else:
			responce_msg_str = json.dumps(responce_msg_json)
		try:
			self.connect()
		except:
			pass

		try:
			self._tcp_socket_handler.send(self._client, responce_msg_str, self._server_public_key, self._my_private_key)
		except:
			print("Endpoint.send_command_res() - Error sending responce")


	def operate(self):
		server_command_msg_json = self.get_command_msg()
		responce_msg_json = self.run_command(server_command_msg_json)
		self.send_command_res(responce_msg_json)





	# def get_run_command(self):
	# 	#get command from server
	# 	self.connect()
	# 	responce = self._client.get_command()
	# 	print(responce)
	# 	if responce != None:
	# 		result, exit_code = self._agent.run_command(responce["command"])
	# 		# print(result)
	# 		# command_id, stdout, stderr=""
	#
	# 		print(f"responce['command_id'] = {responce['command_id']}")
	# 		#add stderrr
	# 		self._client.send_results(responce["command_id"], exit_code, result)
	# 	else:
	# 		print("run_local_command: None")

		#run command
		#send results back to the server
	#
	# def ready_accept(self):
	# 	self._client.connect()


if __name__ == "__main__":
	pass
