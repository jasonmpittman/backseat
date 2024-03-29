from shared import tcp_socket_handler

from backseat_server import client_handler

import json

from backseat_server import server_message

import threading

from shared import log_handler

import sys

import traceback

from exceptions.server_restart_exception import ServerRestartException


class ServerLoop():
	"""
	This class handles the server looping that is needed to be done. This includes, multithreading and client handling.

	Attributes
	----------
	_socket_handler : TcpSocketHandler object
	_cli_handler : ClientHandler object
	_server_msg : ServerMessage object
	_server : Socket object - bound and listening
	_client : str
	_src_ip : str
	_server_public_key : str
	_server_private_key : str
	"""
	def __init__(self, ip, port, allowed_connections, server_private_key, server_public_key, server_info):
		"""
		Attributes are initialized.

		Parameters
		----------
		ip : str
		port : int
		allowed_connections : int
		"""
		# change these to server_public and server_private
		self._server_private_key = server_private_key
		self._server_public_key = server_public_key

		self._socket_handler = tcp_socket_handler.TcpSocketHandler(self._server_private_key, self._server_public_key)
		self._server_info = server_info
		self._cli_handler = client_handler.ClientHandler(self._server_public_key, self._server_info)
		self._server_msg = server_message.ServerMessage()
		self._server = self._socket_handler.create_server(ip, port, allowed_connections)
		self._client = None
		self._src_ip = None
		self._log = log_handler.LogHandler("ServerLoop")
		self._log.info("__init__", "Server setup and ready to go.")


	def server_iteration(self):
		"""
		This function represents a single iteration of going through the
		server_loop. A thread runs this function, upon completion it is
		terminated.

		Parameters
		----------
		"""

		theard_id = threading.get_ident()
		self._log.info("server_iteration", f"Thread ID = {theard_id}")
		print("client:\n", self._client)
		res, sender_key = self._socket_handler.recieve(self._client)
		print(sender_key)
		print(res)

		self._log.info("server_iteration", f"Message recieved from {sender_key}")

		print(f"Sender - {sender_key}\n{res}")
		print("----")
		res_dict = json.loads(res)

		next_depot_item, count = self._cli_handler.client_handler(res_dict, sender_key)

		if next_depot_item != None:
			if next_depot_item == "depot_item_added":
				print("DEPOT ITEM ADDED")
				return None

			elif next_depot_item == "checked_off_depot_item":
				print("DEPOT ITEM CHECKEDOFF")
				return None


			elif next_depot_item == "get_server_data" or next_depot_item == "get_startup_data":
				server_data = count
				self._socket_handler.send(self._client, server_data, self._server_public_key)
				return None

			elif next_depot_item == "server_restart":
				raise ServerRestartException()

			else:
				print(next_depot_item)
				responce_msg_json = self._server_msg.create_msg(False, next_depot_item["command"], False, "", 0, next_depot_item["depot_count"], next_depot_item["command_id"])
				self._log.info("server_iteration", "Message is created for a new depot item")
		else:
			responce_msg_json = self._server_msg.create_msg(True, "", False, "", 0, count, 0)
			self._log.info("server_iteration", "Message is created letting the endpoint know there is not a new depot item")

		self._socket_handler.send(self._client, responce_msg_json, sender_key)
		self._log.info("server_iteration", "Message is sent")

	def server_loop(self):
		"""
		Looping mechanism of the server. If the loop_iteration is the inside of
		the loop, then this is the outside of the loop that actually drives
		loop_iteration.

		Parameters
		----------
		"""
		try:
			print("--Server Running--")
			while True:
				try:
					self._client, self._src_ip = self._server.accept()
					new_thread = threading.Thread(target=self.server_iteration())
					new_thread.start()
					self._log.info("server_loop", "Thread successfully ran")
				
				except ServerRestartException as E:
					self.socket_close()
					raise
				
				except KeyboardInterrupt as E:
					raise

				except Exception as E:
					print("--Error in server_loop threading--")
					print(E)
					_, _, tb = sys.exc_info()
					traceback.print_tb(tb)
					print("-- --")
					self._log.error("server_loop", f"Error in threading: {E}")

		except ServerRestartException as E:
			raise

		except KeyboardInterrupt:
			print("\n--Keyboard Interrupt--")
			self.socket_close()

			self._log.info("server_loop", "-- Keyboard Interrupt --")
			raise
	
	def server_shutdown(self):
		print("Server Shutdown")

	def socket_close(self):
		self._server.close()
		if self._client != None:
			self._client.close()		
