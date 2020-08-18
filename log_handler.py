'''
Handles all the logging.
'''
import logging

class LogHandler:
	def __init__(self, name):
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.INFO)
		self.file_handler = logging.FileHandler("Logfile.log")
		self.formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s:%(message)s")
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)

	def info(self, class_name, fuction_name, message):
		self.logger.info(f"{class_name}.{function_name} - {message}")

	def warning(self, class_name, function_name, message):
		self.logger.warning(f"{class_name}.{function_name} - {message}")

	def error(self, class_name, function_name, message):
		self.logger.error(f"{class_name}.{function_name} - {message}")
