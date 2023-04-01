from typing import List
import requests

class PiPDU:
    host: str
    apiPort: int
    apiURL: str
    metricsPort: int
    metricsURL: str

    def __init__(self, certificate: str, host: str, apiPort: int = 3000, metricsPort: int = 8000):
        self.host = host
        self.apiPort = apiPort
        self.metricsPort = metricsPort
        self.apiURL = f"http://{self.host}:{self.apiPort}/api/v1"
        self.metricsURL = f"http://{self.host}:{self.metricsPort}"
