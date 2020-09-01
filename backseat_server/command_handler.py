'''
Handles command creation
'''
from backseat_server import depot
from backseat_server import registration_handler


class CommandHandler:
	#possibly ping those hosts that are in restmode waiting for responce
	def __init__(self):
		self._depot_list = depot.DepotList()
		self._registration = registration_handler.RegistrationHandler()
		for host in self._registration.host_list:
			self._depot_list.add_depot(host["FQDN"])

	def add_to_all(self, command):
		self._depot_list.add_to_all(command)

	def add_command_all_os(self, command, OS):
		host_list = self._registration.get_hosts(OS)
		self._depot_list.add_to_specified(command, host_list)

	def add_command_to_specified(self, command, host_list):
		self._depot_list.add_to_specified(command, host_list)
