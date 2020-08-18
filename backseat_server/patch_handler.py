'''
Handles everything involved with patches, gets them, and creates installation commands.

Interfaces with websites that have lists of security issues in software and OS's.
'''
class PatchHandler:
	def __init__(self, depot_list):
		self._depot_list = depot_list
