from backseat_server.depot_files import depot_list

from shared import log_handler

from backseat_server import command_handler

from shared import read_host_config

class ClientHandler:
	"""
	This is the logical backend to the functionality of the server. The messages
	are sent here for processing. The messages are deconstructed and the
	necissary subsystems are run.

	Attributes
	----------
	depot_list : DepotList object
	"""
	def __init__(self, server_public_key, server_info):
		"""
		Initializes the depot list.

		Parameters
		----------
		"""
		self._server_info = server_info
		self._server_public_key = server_public_key
		self.depot_list = depot_list.DepotList()
		self._command_handler = command_handler.CommandHandler(self.depot_list)
		
		self._log = log_handler.LogHandler("ClientHandler")
		self._host_config = read_host_config.ReadHostConfig()
		self._key_table = self._host_config.get_key_table()
		#for testing
		working_depot = self.depot_list.get_working_depot(self._key_table["client1_public.pem"])
		working_depot.add("ls -al", 100)
		working_depot.add("PWD", 101)
	
	def _server_client_handler(self, client_dict, sender_key):
		print("SERVER SENDER KEY")
		if client_dict["type"] == "add":
			self._command_handler.add_command_to_specified(client_dict["command"], client_dict["who"])
			print("### - added to depot - ###")
			print(self.depot_list.get_depot_list_info())
			return "depot_item_added", -1
			
		if client_dict["type"] == "checkoff":
			print("In checkout code")
			self._command_handler.checkoff_command(client_dict["who"], client_dict["command_id"])
			return "checked_off_depot_item", -1

		if client_dict["type"] == "get_server_data":
			print("Get Server Data")
			self._server_info.update_depots_state(self.get_depots_data())
			output = self._server_info.to_json()
			print("--server_info--")
			print(output)
			return "get_server_data", output
		
		if client_dict["type"] == "get_startup_data":
			print("Get Startup Data")
			json_static_endpoint_data = self._server_info.get_static_endpoint_data()
			return "get_startup_data", json_static_endpoint_data

		if client_dict["type"] == "server_restart":
			print("Server restart")
			return "server_restart", -1

		print("Recieved message from server, but 'type' is not 'add' or 'checkoff'.")

		return None
	
	def _client_ping(self, client_dict, working_depot):
		self._log.info("client_handler", "ping == False")
		if client_dict["completed"]:
			self._log.info("client_handler", "completed == True")
			if client_dict["successful"]:
				self._log.info("client_handler", "successful == True")
				depot_item = working_depot.get_by_id(client_dict["command_id"])
				if depot_item is not None:
					# sets the valus of depot item because the depot_item is completed
					depot_item.set(client_dict["completed"], client_dict["stdout"], client_dict["exit_code"])
					# print(f"Modified Depot Item: {depot_item.output()}")
					self._server_info.update_last_successful_job(depot_item.output())
					working_depot.count -= 1
					self._log.info("client_handler", "depot item information updated")
				else:
					# is unable to obtain the depot_item by id
					self._log.error("client_handler", "Could not find depot item by that id - returning: None, -1")
					return None, -1
			else:
				#if unsequenced go onto the next item (table this one until the user has ruled on it), else wait for user responce
				# The command was not successful
				self._log.error("client_handler", "Command was not successful")
		else:
			# This should not happen
			self._log.info("command_handler", "Command not completed")

	def client_handler(self, client_dict, sender_key):
		"""
		Decides what subsystem should run based on what message the client has
		sent to the server.

		Parameters
		----------
		client_dict : python dict
		sender_key : str
		"""
		#gets working depot

		if sender_key == self._server_public_key:
			return self._server_client_handler(client_dict, sender_key)
			

		self._server_info.update_heatbeat()
		print("-------")
		print(type(client_dict))
		working_depot = self.depot_list.get_working_depot(sender_key)

		if client_dict["ping"] == False:
			return self._client_ping(client_dict, working_depot)
		else:
			# Pinging the server to figure out if there is a command that can be picked up
			self._log.info("command_handler", "Ping == True")
		print("-----@@@@@@@@-----")
		working_depot.print_depot_contents()
		if client_dict["ready"] and working_depot.count > 0:
			self._log.info("command_handler", "Ready!")
			return working_depot.get_next(), working_depot.count
		else:
			self._log.info("command_handler", "Not ready - Returned None and working_depot count")
			return None, working_depot.count

	def add_commands(self, client_dict):
		"""
		Adds commands to the depots that are provided to the server.

		Parameters
		----------
		client_dict : python dictionary
		"""
		print("add_command running")
		if client_dict["host_list"] == []:
			self._command_handler.add_to_all(client_dict["command"])
		else:
			self._command_handler.add_command_to_specified(client_dict["command"], client_dict["host_list"])
			print(self.get_depots_data())


	def checkoff_command(self, client_dict):
		"""
		Checks off a command that the user wants to override as completed, even if it has not been completed.

		Parameters
		----------
		client_dict : python dictionary
		"""

		self._command_handler.checkoff_command(client_dict["who"], client_dict["command_id"])
		return "checked_off_depot_item", -1

	def get_depots_data(self):
		"""
		Gets all the depot item data and puts it into a list which it returns.

		Parameters
		----------
		"""
		depots_out = []
		for depot in self.depot_list.list:
			i_list = []
			depot_item_list = {}
			for depot_item in depot.depot_items_list:
				i_list.append(depot_item.get_info())
			depot_item_list = {"host": depot.host, "name": depot.name, "count": depot.count, "item_list": i_list}
			depots_out.append(depot_item_list)
		return depots_out
