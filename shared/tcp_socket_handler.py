#!/usr/bin/env python3

__author__ = "Kevin A. Rubin, Jason M. Pittman"
__copyright__ = "Copyright 2020"
__credits__ = ["Kevin A. Rubin, Jason M. Pittman"]
__license__ = "AGPLv3"
__version__ = "1.0.0"
__maintainer__ = "Jason M. Pittman"
__email__ = "jpittman@highpoint.edu"
__status__ = "Release"
__dependecies__ = "socket, asym_cryptography_handler, os, log_handler"

import socket

from shared import asym_cryptography_handler as crypto

import os

from shared import log_handler


class TcpSocketHandler:
	"""
	This class is made to handle all of the TCP communication that occurs in
	the backseat application. These functions can be used by both the endpoint
	and the server to send messages. This handles all of the encryption and can
	handle text of arbitrary length.

	Attributes
	----------
	_crypto : cryptography module object
	send : function
	export : function
	recieve : function
	_byte_splitter : function
	_get_key_list : function
	_identify : function
	"""
	def __init__(self, my_private_key, my_public_key):
		"""
		Instantiates an object from the encryption module.

		Parameters
		----------
		"""
		self._crypto = crypto.AsymmetricCryptographyHandler()
		self._log = log_handler.LogHandler(self.__class__.__name__)
		self._my_private_key = my_private_key
		self._my_public_key = my_public_key

	def send(self, client, message, public_key):
		"""
		This function sends the provided message to the provide client
		connection after encrypting the message using the public key and
		signing it using the private key.

		Parameters
		----------
		client : socket connection object
		message : str
		public_key : str
		"""
		blocks = self._create_message_blocks(message)
		cyphertext_full_msg = b''
		try:
			for block in blocks:
				cyphertext = self._crypto.encrypt(block, public_key)
				cyphertext_full_msg += cyphertext
			self._log.info("send", "Blocks encrypted")
		except:
			self._log.error("send", "Failed to encrypt blocks - returned None")
			print("failed to make encrypted blocks")
			return None
		try:
			signature = self._crypto.sign(cyphertext_full_msg, self._my_private_key)
			signed_msg = cyphertext_full_msg + signature
			self._log.info("send", "Message signed")
		except:
			self._log.error("send", "Failed to sign message - returned None")
			return None
		try:
			client.send(signed_msg)
			client.shutdown(socket.SHUT_WR)
			self._log.info("send", "Message sent")
		except:
			self._log.error("send", "Failed to send message - returned None")
			return None


	def recieve(self, client):
		"""
		This function recieves the entire message sent, then it decrypts it and
		finds out who signed the message. Returns decrypted message and name of
		the sender's public key.

		Parameters
		----------
		client : socket connection object
		"""
		signed_msg = b''
		return_msg = r""
		try:
			while True:
				raw_msg = client.recv(1024)
				if not raw_msg:
					break
				signed_msg += raw_msg
			self._log.info("recieve", "Full message recieved")
		except:
			self._log.error("recieve", "Failed to recieve message - returned None")
			return None
		client_msg = signed_msg[:-256]
		client_signature = signed_msg[-256:]
		sender_public_key = self._identify(client_msg, client_signature)
		print("sender public key: ", sender_public_key)
		msg_byte_blocks = self._byte_splitter(client_msg)
		self._log.info("recieve", "Message prepared for decryption")
		try:
			for block in msg_byte_blocks:
				return_msg += self._crypto.decrypt(block, self._my_private_key)
			self._log.info("recieve", "Message fully decrypted")
		except:
			self._log.error("recieve", "Failed to decrypt message - retuned None")
			return None
		return return_msg, sender_public_key


	def create_client_socket_connect(self, ip, port):
		"""
		This function creates a socket connection object using the ip and port
		provided to it. It then returns that object if it is successful in
		creation.

		Parameters
		----------
		ip : str
		port : int
		"""
		try:
			connected_socket = socket.socket()
			connected_socket.connect((ip, port))
			self._log.info("create_client_socket_connect", "Client socket created and connected")
			return connected_socket
		except:
			self._log.error("create_client_socket_connect", "Failed to connect to (ip[{ip}], port[{port}]) - returned None")
			return None

	def create_server(self, ip, port, total_connections):
		"""
		This creates a server socket, binds it to the provided port and ip,
		then sets it to listen.

		The server is returned if it is successful, and None is if it failed.

		Parameters
		----------
		ip : str
		port : int
		total_connections : int
		"""
		try:
			server = socket.socket()
			try:
				server.bind((ip, port))
			except Exception as Ex:
				print("Bind Failed")
				print(Ex)

				_, _, tb = sys.exc_info()
				traceback.print_tb(tb)
				self._log.error("create_server", "Server faild to bind")
				return None
			try:
				server.listen(total_connections)
			except Exception as Ex:
				print("Listen Failed")
				print(Ex)
				_, _, tb = sys.exc_info()
				traceback.print_tb(tb)
				self._log.error("create_server", "Server failed to listen")
				return None
			self._log.info("create_server", "Server created, bound, and listening")
			return server
		except Exception as E:
			print(E)
			_, _, tb = sys.exc_info()
			traceback.print_tb(tb)
			self._log.error("create_server", f"Failed to create, bind, or listen to (ip[{ip}], port[{port}]) - returned None")
			print(f"Failed to create, bind, or listen to (ip[{ip}], port[{port}]) - returned None")
			return None

	def _create_message_blocks(self, message):
		"""
		This function cuts the message into 245 character blocks and puts them
		into a list. This is for the purpose of encrytion which only accepts
		strings less than or equal to 245 in length.

		Parameters
		----------
		message : str
		"""
		chunk_list = [message[i:i+245] for i in range(0, len(message), 245)]
		self._log.info("_create_message_blocks", "Message cut into blocks")
		return chunk_list

	def _byte_splitter(self, message):
		"""
		This function cuts the recievedmessage into 245 byte blocks and puts
		them into a list. This is for the purpose of decryption and separating
		the cryptograhic signture from the message.

		Parameters
		----------
		message : str
		"""
		chunk_list = [message[i:i+256] for i in range(0, len(message), 256)]
		self._log.info("_byte_splitter", "Raw message cut into 256 byte blocks")
		return chunk_list

	def _get_key_list(self):
		"""
		Gets a list of the keys that the running program has access to in the
		keys directory.

		Parameters
		----------
		"""
		output_arr = []
		arr = os.listdir("keys")
		for item in arr:
			s_item = item.split("_")
			if s_item[1] == "public.pem":
				output_arr.append(item)

		self._log.info("_get_key_list", "Retuned a list of key names")
		return output_arr

	def _identify(self, obj, signature):
		"""
		This function identifies who sent the message based on the signature in
		public key encryption.

		Parameters
		----------
		obj : bytes
		signature : bytes
		"""
		key_list = self._get_key_list()
		print(key_list)
		for key in key_list:
			if self._crypto.is_sign_valid(obj, signature, key) == True:
				self._log.info("_identify", f"Key found [{key}]")

				return key
		self._log.error("_identify", "Cound not find key - returned None")
		print("Could not find key - returned none")
		return None
