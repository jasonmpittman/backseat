'''
Handles command creation
'''
from backseat_server import depot


class CommandHandler:
	#possibly ping those hosts that are in restmode waiting for responce
	def __init__(self):
		self._depot_list = depot.DepotList()
