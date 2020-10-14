from backseat_server import depot

from shared import log_handler

class ClientHandler:
	"""
	This is the logical backend to the functionality of the server. The messages
	are sent here for processing. The messages are deconstructed and the
	necissary subsystems are run.

	Attributes
	----------
	depot_list : DepotList object
	"""
	def __init__(self):
		"""
		Initializes the depot list.

		Parameters
		----------
		"""
		self.depot_list = depot.DepotList()
		working_depot = self.depot_list.get_working_depot("client1_public.pem")
		self._log = log_handler.LogHandler("ClientHandler")
		#for testing
		working_depot.add("ls -al")
		working_depot.add("PWD")
		working_depot.add("fail")

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
		print("-------")
		print(type(client_dict))
		working_depot = self.depot_list.get_working_depot(sender_key)

		if client_dict["ping"] == False:
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
						working_depot.count -= 1
						self._log.info("client_handler", "depot item information updated")
					else:
						# is unable to obtain the depot_item by id
						print()
						self._log.error("client_handler", "Could not find depot item by that id - returning: None, -1")
						return None, -1
				else:
					#if unsequenced go onto the next item (table this one until the user has ruled on it), else wait for user responce
					# The command was not successful
					self._log.error("client_handler", "Command was not successful")
			else:
				# This should not happen
				self._log.info("command_handler", "Command not completed")
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
