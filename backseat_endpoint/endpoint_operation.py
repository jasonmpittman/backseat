from backseat_endpoint import agent

from shared import tcp_socket_handler

from backseat_endpoint import endpoint_message

import json

import time

import threading

import sys

class EndpointOperation:
	"""
	This class handles the full operations of the endpoint.

	Attributes
	----------
	_agent : Agent object
	_tcp_socket_handler : TcpSocketHandler object
	_ip : str
	_port : int
	_client : socket connection object
	_my_private_key : str
	_my_public_key : str
	_server_public_key : str
	_endpoint_msg : EndpointMessage object

	"""
	def __init__(self, serv_ip, serv_port, my_private_key, my_public_key, server_public_key):
		"""
		This function sets up the Endpoint object, so that it can function
		correctly.

		Parameters
		----------
		serv_ip : str
		serv_port : int
		my_private_key : str
		my_public_key : str
		server_public_key : str
		"""
		self._my_private_key = my_private_key
		self._my_public_key = my_public_key
		self._agent = agent.Agent()
		self._tcp_socket_handler = tcp_socket_handler.TcpSocketHandler(self._my_private_key, self._my_public_key)
		self._ip = serv_ip
		self._port = serv_port
		self._client = None
		#Add something to the config file to deal with these
		self._server_public_key = server_public_key
		self._endpoint_msg = endpoint_message.EndpointMessage()


	def connect(self):
		"""
		Creates a TCP socket connection with the server.

		Parameters
		----------
		"""
		self._client = self._tcp_socket_handler.create_client_socket_connect(self._ip, self._port)

	def get_command_msg(self):
		"""
		Creates and sends a message to the server, prompting it to give it the next command. It returns the responce from the server.
		"""
		try:
			self.connect()
		except:
			pass
		message = self._endpoint_msg.get_ping_msg()
		print("Message being sent:")
		print(message)
		print("---")
		self._tcp_socket_handler.send(self._client, message, self._server_public_key)

		responce, sender_key = self._tcp_socket_handler.recieve(self._client)
		print("--responce--")
		print(responce)
		print("--")
		if responce == None:
			print("responce = None")
		else:
			dict_responce = json.loads(responce)
		return dict_responce

	def run_command(self, command_msg_dict):
		"""
		This function processes the command sent to the endpoint from the server, then creates a responce message to the server. The responce is returned in json format.

		Parameters
		----------
		command_msg_dict : python dictionary
		"""
		print(command_msg_dict)
		if command_msg_dict["not_ready"]:
			return None

		responce_msg_json = None

		stdout, stderr, exitcode = self._agent.run_command(command_msg_dict["command"])

		ready = False
		completed = False

		if exitcode != None:
			ready = True
			completed = True

		if exitcode == 0:
			successful = True
		else:
			successful = False

		ping = False

		responce_msg_json = self._endpoint_msg.create_msg(ping, ready, completed, stdout, stderr, successful, exitcode, command_msg_dict["command_id"])

		return responce_msg_json

	def send_command_res(self, responce_msg_json):
		"""
		This function takes in a responce message in json format then sends it to the server.

		Paremeters
		----------
		responce_msg_json :  
		"""
		if responce_msg_json == None:
			print("responce_msg_json = None")
		else:
			# responce_msg_str = json.dumps(responce_msg_json)
			print("########")
			print(responce_msg_json)
			pass
		try:
			self.connect()
		except:
			print("no connection needed / connection failed")

		try:
			self._tcp_socket_handler.send(self._client, responce_msg_json, self._server_public_key)
		except:
			print("Endpoint.send_command_res() - Error sending responce")


	def operate(self):
		server_command_msg_json = self.get_command_msg()
		responce_msg_json = self.run_command(server_command_msg_json)
		if responce_msg_json != None:
			self.send_command_res(responce_msg_json)
		else:
			print("run_command == None, server is probably not ready")

	def operation_iteration(self):
		try:
			self.operate()
			print("1")
			time.sleep(1)
			print("2")
			time.sleep(1)
			print("3")
			time.sleep(1)
			print("Go!")
			return True
		except:
			return False

	def operation_loop(self):
		working = True
		try:
			print("-- Endpoint Loop running --")
			while working:
				working = self.operation_iteration()
			print("-- Server disconnected --")
		except KeyboardInterrupt:
			print("\n--Keyboard Interrupt--")

	def thread_operation_loop(self):
		loop_thread = threading.Thread(target=self.operation_loop)
		loop_thread.daemon = True
		loop_thread.start()


if __name__ == "__main__":
	pass
