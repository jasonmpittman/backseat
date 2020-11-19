from backseat_endpoint import agent

from backseat_endpoint import endpoint_message

from shared import tcp_socket_handler

from shared import log_handler

import json

import time

import threading

import sys

class EndpointOperation:
	"""
	This class handles the full operations of the endpoint.

	Attributes
	----------
	_my_private_key : str
	_my_public_key : str
	_agent : Agent object
	_tcp_socket_handler : TcpSocketHandler object
	_ip : str
	_port : int
	_my_ip : str
	_my_port : int
	_my_total_connections : int
	_client : socket connection object
	_server_public_key : str
	_endpoint_msg : EndpointMessage object
	_f_server : a running TcpSocketHandler server
	_f_client : a TCP connection

	"""
	def __init__(self, serv_ip, serv_port, my_ip, my_port, my_private_key, my_public_key, server_public_key):
		"""
		This function sets up the Endpoint object, so that it can function
		correctly.

		Parameters
		----------
		serv_ip : str
		serv_port : int
		my_ip : str
		my_port : int
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
		self._my_ip = my_ip
		self._my_port = my_port
		self._my_total_connections = 10
		self._client = None
		#Add something to the config file to deal with these
		self._server_public_key = server_public_key
		self._endpoint_msg = endpoint_message.EndpointMessage()
		self._f_server = None
		self._f_client = None
		self._log = log_handler.LogHandler("EndpointOperation")


	def connect(self):
		"""
		Creates a TCP socket connection with the server.

		Parameters
		----------
		"""
		try:
			self._client = self._tcp_socket_handler.create_client_socket_connect(self._ip, self._port)
			self._log.info("connect", "Created connection")
		except Exception as E:
			_, _, tb = sys.exc_info()
			traceback.print_tb(tb)
			print("E")
			self._log.info("connect", f"Failed to connect: {E}")

	def get_command_msg(self):
		"""
		Creates and sends a message to the server, prompting it to give it the next command. It returns the responce from the server.
		"""
		try:
			self.connect()
		except Exception as E:
			print(E)
		message = self._endpoint_msg.get_ping_msg()
		try:
			self._tcp_socket_handler.send(self._client, message, self._server_public_key)
		except Exception as E:
			print(E)
			self._log.warning("get_command_msg", f"Sending error: {E}")

		try:
			responce, sender_key = self._tcp_socket_handler.recieve(self._client)
			if sender_key != self._server_public_key:
				print("Sender not server -- Returned None")
				return None
			print("--responce--")
			print(responce)
			print("--")
			if responce == None:
				print("responce = None")
			else:
				dict_responce = json.loads(responce)
			return dict_responce
		except Exception as E:
			print(E)
			self._log.warning("get_command_msg", f"Exception: {E}")
			return

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

		stdout, stderr, exitcode = self._agent.run_command(command_msg_dict["command"], command_msg_dict["password"])

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
		"""
		This function at a high level deals with performing the actual steps of getting, running, then responding to commands provided.

		Parameters
		----------
		"""
		server_command_msg_json = self.get_command_msg()
		responce_msg_json = self.run_command(server_command_msg_json)
		if responce_msg_json != None:
			self.send_command_res(responce_msg_json)
		else:
			print("run_command == None, server is probably not ready")

	def operation_iteration(self):
		"""
		This function spaces out operating of the program to simulate the heartbeats.

		Parameters
		----------
		"""
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
		"""
		Loops the operation of the program. This is the master loop of the endpoint.

		Parameters
		----------
		"""
		working = True
		try:
			print("-- Endpoint Loop running --")
			while working:
				working = self.operation_iteration()
			print("-- Server disconnected --")
		except KeyboardInterrupt:
			print("\n--Keyboard Interrupt--")

	def thread_operation_loop(self):
		"""
		Threads the operation so that the endpoint has the ability to run other services at the same time.

		Parameters
		----------
		"""
		print("Prethread write")
		loop_thread = threading.Thread(target=self.operation_loop)
		print("Prethread start")
		loop_thread.start()
		print("problem in force")
		force_run_thread = threading.Thread(target=self.force_run_server)
		force_run_thread.start()
		print("Past force")


	def force_run_server(self):
		self._f_server = self._tcp_socket_handler.create_server(self._my_ip, self._my_port, self._my_total_connections)
		try:
			while True:
				print("###-- Waiting for force command --###")
				self._f_client, _ = self._server.accept()
				try:
					new_thread = threading.Thread(target=self.operate())
					new_thread.start()
				except Exception as E:
					print("--Error in force_run_server threading--")
					print(E)
					_, _, tb = sys.exc_info()
					traceback.print_tb(tb)
		except KeyboardInterrupt:
			print("\n--Keyboard Interrupt--")
			self._f_server.close()
			if self._f_client != None:
				self._f_client.close()

#Server does not know about the IP of the endpoint...

if __name__ == "__main__":
	pass
