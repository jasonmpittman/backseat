import socket

from shared import asym_cryptography_handler as crypto

import os

# AsymmetricCryptographyHandler()
# Note on the asym_crypto:
	# 245 character encrytion limit
	# 256 byte encryption output
	# 256 byte signature output


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
	def __init__(self):
		"""
		Instantiates an object from the encryption module.

		Parameters
		----------
		"""
		self._crypto = crypto.AsymmetricCryptographyHandler()

	def send(self, client, message, public_key, private_key):
		"""
		This function sends the provided message to the provide client
		connection after encrypting the message using the public key and
		signing it using the private key.

		Parameters
		----------
		client : socket connection object
		message : str
		public_key : str
		private_key : str
		"""
		blocks = self._create_message_blocks(message)
		cyphertext_full_msg = b''
		try:
			for block in blocks:
				cyphertext = self._crypto.encrypt(block, public_key)
				cyphertext_full_msg += cyphertext
		except:
			print("TcpSocketHandler.send(): error in encrypting blocks")
			return None
		try:
			signature = self._crypto.sign(cyphertext_full_msg, private_key)
			signed_msg = cyphertext_full_msg + signature
		except:
			print("TcpSocketHandler.send(): Error in signing message")
			return None
		try:
			client.send(signed_msg)
			client.shutdown(socket.SHUT_WR)
		except:
			print("TcpSocketHandler.send(): Error in sending message")
			return None


	def recieve(self, client, private_key):
		"""
		This function recieves the entire message sent, then it decrypts it and
		finds out who signed the message. Returns decrypted message and name of
		the sender's public key.

		Parameters
		----------
		client : socket connection object
		private_key : str
		"""
		signed_msg = b''
		return_msg = r""
		try:
			while True:
				raw_msg = client.recv(1024)
				if not raw_msg:
					break
				signed_msg += raw_msg
		except:
			print("TcpSocketHandler.recieve(): Error in recieving message")
			return None
		client_msg = signed_msg[:-256]
		client_signature = signed_msg[-256:]
		sender_public_key = self._identify(client_msg, client_signature)
		print("sender public key: ", sender_public_key)
		msg_byte_blocks = self._byte_splitter(client_msg)

		try:
			for block in msg_byte_blocks:
				return_msg += self._crypto.decrypt(block, private_key)
				print("--return_msg--")
				print(return_msg)
		except:
			print("TcpSocketHandler.recieve(): Error in decryption of the message")
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
			return connected_socket
		except:
			print(f"Failed to connect to (ip[{ip}], port[{port}])")
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
			server.bind((ip, port))
			server.listen(total_connections)
			return server
		except:
			print(f"Failed to create, bind, or listen to (ip[{ip}], port[{port}])")
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
		return chunk_list

	def _get_key_list(self):
		"""
		Gets a list of the keys that the running program has access to in the
		keys directory.

		Parameters
		----------
		"""
		arr = os.listdir("keys")
		return arr

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
		print(f"key_list: {key_list}")
		print(f"obj: {obj}")
		print(f"signature: {signature}")
		for key in key_list:
			if self._crypto.is_sign_valid(obj, signature, key) == True:
				return key
		return None
