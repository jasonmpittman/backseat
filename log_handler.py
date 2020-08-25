'''
Handles all the logging.
'''
import logging

class LogHandler:
	def __init__(self, name, class_name):
		self._class = class_name
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.INFO)
		self.file_handler = logging.FileHandler("Logfile.log")
		self.formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s:%(message)s")
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)

	def info(self, fuction_name, message):
		self.logger.info(f"{self._class}.{function_name} - {message}")

	def warning(self, function_name, message):
		self.logger.warning(f"{self._class}.{function_name} - {message}")

	def error(self, function_name, message):
		self.logger.error(f"{self._class}.{function_name} - {message}")

if __name__ == "__main__":
	pass
