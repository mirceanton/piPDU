from typing import List
import requests

class PiPDU:
    host: str
    apiPort: int
    apiURL: str
    metricsPort: int
    metricsURL: str

    def getGlobalMetrics(self) -> float:
        pass

    def getMetricsFor(self, socket_id: int) -> List[float]:
        pass

    def getStateFor(self, socket_id: int) -> bool:
        pass

    def setStateFor(self, socket_id: int, socket_state: bool) -> None:
        pass

    def testConnection(self) -> bool:
        url = f"{self.baseURL}/ping"
        response = requests.get(url, verify=False)
        return response.status_code == 200

    def __init__(self, certificate: str, host: str, apiPort: int = 3000, metricsPort: int = 8000):
        self.host = host
        self.apiPort = apiPort
        self.metricsPort = metricsPort
        self.apiURL = f"http://{self.host}:{self.apiPort}/api/v1"
        self.metricsURL = f"http://{self.host}:{self.metricsPort}"
