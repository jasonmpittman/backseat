'''
Handles all the logging.
'''
import logging

class LogHandler:
	def __init__(self, class_name):
		'''
		Input: class_name (str): name of the class that the logger is in

		Initializes all important parts of the LogHandler. Sets up formatting and logger parts.
		'''
		self._class_name = class_name
		self.logger = logging.getLogger(self._class_name)
		self.logger.setLevel(logging.INFO)
		self.file_handler = logging.FileHandler("Logfile.log")
		self.formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s:%(message)s")
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)

	def info(self, function_name, message):
		'''
		Input:
			function_name (str): name of the function that is running
			message (str): important information that needs to be logged
		Writes an info message to the log file.
		'''
		self.logger.info(f"{self._class_name}.{function_name} - {message}")

	def warning(self, function_name, message):
		'''
		Input:
			function_name (str): name of the function that is running
			message (str): important information that needs to be logged
		Writes a warning message to the log file.
		'''
		self.logger.warning(f"{self._class_name}.{function_name} - {message}")

	def error(self, function_name, message):
		'''
		Input:
			function_name (str): name of the function that is running
			message (str): important information that needs to be logged
		Writes an error message to the log file.
		'''
		self.logger.error(f"{self._class_name}.{function_name} - {message}")

if __name__ == "__main__":
	pass
