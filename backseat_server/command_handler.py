'''
Handles command creation
'''
from backseat_server.depot_files import depot

from backseat_server import registration_handler

from shared import log_handler

class CommandHandler:
	"""
	This deals with the commands by distributing the commands to the different
	depots depending on the situation. Distribution can be done by adding it to
	all depots or specified depots.

	Attributes
	----------
	_depot_list : DepotList object
	_registration : RegistrationHandler object

	"""
	def __init__(self, depot_list):
		"""
		Initializes the self._depot_list and the self._registration.
			- self._depot_list - list of all depots that will be accessed by
			  clients to get commands.
			- self._registration - of RegistrationHandler type, used in order
			  to create depots for the approved hosts.
		Depots for each host are created

		Parameters
		----------
		depot_list : DepotList object
		"""

		self._logger = log_handler.LogHandler(self.__class__.__name__)
		self._depot_list = depot_list
		self._logger.info(self.__init__.__name__, "self._depot_list initialized")

		self._registration = registration_handler.RegistrationHandler()
		self._logger.info(self.__init__.__name__, "self._registration initialized")
		for host in self._registration.host_list:
			self._depot_list.add_depot(host["public_key"], host["name"])
		self._logger.info(self.__init__.__name__, "self._depot_list filled with depots for each approved host")

	def add_to_all(self, command):
		"""
		Adds a command to all depots in self._depot_list.

		Parameters
		----------
		command : str
		"""
		self._depot_list.add_to_all(command)
		self._logger.info(self.add_to_all.__name__, f"Command [{command}] added to all depots")

	def add_command_all_os(self, command, OS):
		"""
		Adds command to all depots for hosts of a provided operating system.

		Parameters
		----------
		command : str
		OS : str
		"""
		hosts = self._registration.get_hosts(OS)
		os_hosts = []
		for host in hosts:
			os_hosts.append(host["FQDN"])
		print(f"Host_list [{os_hosts}]")
		self._depot_list.add_to_specified(command, os_hosts)
		self._logger.info(self.add_command_all_os.__name__, f"Command [{command}] added to all depots of OS [{OS}]")

	def add_command_to_specified(self, command, host_list):
		"""
		Adds command to a list of specified hosts' depots.

		Parameters
		----------
		command : str
		host_list : list
		"""
		if len(host_list) > 0:
			self._depot_list.add_to_specified(command, host_list)
			self._logger.info(self.add_command_to_specified.__name__, f"Added command [{command}] to hosts {host_list}")
		else:
			self.add_to_all(command)

	def print_depots(self):
		"""
		Prints depot contents.

		Parameters
		----------
		"""
		self._depot_list.print_depot_list()

	def checkoff_command(self, depot_name, command_id):
		"""
		This allows commands that cannot or will not complete to be manually overriden so that the next command can run.

		Parameters
		----------
		depot_name : str
		command_id : int
		"""
		working_depot = self._depot_list.get_working_depot(depot_name)
		depot_item = working_depot.get_by_id(command_id)
		#126 -- Command not found error code
		depot_item.set(True, "MANUALLY OVERRIDDEN", 126)
