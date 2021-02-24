from shared import log_handler

class DepotItem:
	"""
	This class keeps track of individual commands, the command id, if the command has been run, the output of the command, and the exit code. These items are put into depots which keep track of which endpoint it belongs to.

	Attributes
	----------
	command : str
	command_id : int
	_done : bool
	_stdout : str
	_exit_code : int
	_item_order : int
	"""
	def __init__(self, command, command_id, item_order):
		"""
		This initializes the creation of a depot item.

		Parameters
		----------
		command : str
		command_id : int
		item_iterator : int
		"""
		self._log = log_handler.LogHandler("DepotItem")
		self.command = command
		self.command_id = command_id
		self._done = False
		self._stdout = ""
		self._exit_code = None
		self._log.info("__init__", f"DepotItem created: {command} {command_id}")
		self._item_order = item_order

	def set(self, done, stdout, exit_code):
		"""
		This function sets the values for a command that has already ran.

		Parameters
		----------
		done : bool
		stdout : str
		exit_code : int
		"""
		self._done = done
		self._stdout = stdout
		self._exit_code = exit_code
		self._log.info("set", f"Item with command_id={self.command_id}, values set. done={done} stdout={stdout} exit_code={exit_code}")

	def output(self):
		"""
		This function returns all the attributes of a DepotItem as a string.

		Parameters
		----------
		"""
		self._log.info("output", f"Returning DepotItem with command_id [{self.command_id}] values as a string")
		return f"Command:{self.command}\n Command ID: {self.command_id}\n Done: {self._done}\n stdout: {self._stdout}\n Exit Code: {self._exit_code}\n item_iterator: {self._item_order}\n"

	def get_info(self):
		return {"command": self.command, "command_id": self.command_id, "done": self._done, "stdout": self._stdout, "exit_code": self._exit_code, "item_iterator": self._item_order}
