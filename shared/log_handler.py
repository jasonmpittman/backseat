'''
Handles all the logging.
'''
import logging

class LogHandler:
	def __init__(self, class_name):
		self._class_name = class_name
		self.logger = logging.getLogger(self._class_name)
		self.logger.setLevel(logging.INFO)
		self.file_handler = logging.FileHandler("Logfile.log")
		self.formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s:%(message)s")
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)

	def info(self, function_name, message):
		self.logger.info(f"{self._class_name}.{function_name} - {message}")

	def warning(self, function_name, message):
		self.logger.warning(f"{self._class_name}.{function_name} - {message}")

	def error(self, function_name, message):
		self.logger.error(f"{self._class_name}.{function_name} - {message}")

if __name__ == "__main__":
	pass
