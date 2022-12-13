import re
import requests
from common.config import Config

class Metrics:
	# Singleton instance of the Metrics class
	__instance = None

	# PiPDU server prometheus metrics endpoint
	__metrics_url = f"http://{Config().api.host}:{Config().api.port}/metrics"

	# The array containing the metrics values for each socket
	metrics = []

	# The overall consumption, sum of all metrics
	total = 0

	# Refresh the metrics array with values from the Prometheus endpoint
	def collect(self):
		# Clean up the metrics
		self.metrics = []
		self.total = 0

		# Scrape the metrics endpoint
		response = requests.get(self.__metrics_url)

		# Extract only the values for the sockets
		for line in response.text.split("\n"):
			if re.search("^socket_", line):
				value = float(line.split(' ')[1])
				self.metrics.append(value)
				self.total += value

	# Method for creating a singleton instance of the Metrics class
	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super().__new__(cls)
		return cls.__instance
