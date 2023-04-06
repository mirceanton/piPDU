from typing import List
from prometheus_client.parser import text_string_to_metric_families
import requests
import json


class PiPDU:
    name: str
    host: str
    apiPort: int
    metricsPort: int

    def getGlobalMetrics(self) -> List[float]:
        response = requests.get(self.metricsURL)
        metrics = text_string_to_metric_families(response.text)

        # Extract the gauges from the metrics
        gauges = [metric for metric in metrics if metric.type ==
                  'gauge' and metric.name.startswith('socket_')]

        # Extract the values of the socket gauges
        socket_values = [0] * len(gauges)
        for gauge in gauges:
            socket_id = int(gauge.name.split('_')[1])
            socket_values[socket_id] = gauge.samples[0].value

        # Return the list of socket values
        return socket_values

    def getMetricsFor(self, socket_id: int) -> float:
        return self.getGlobalMetrics()[socket_id]

    def getStateFor(self, socket_id: int) -> bool:
        url = f"{self.apiURL}/socket/{socket_id}/info"
        response = requests.get(url, verify=self.ssl)

        if (response.status_code != 200):
            raise RuntimeError(
                f'Failed to get socket status: {response.status_code} ({response.text})'
            )

        data = json.loads(response.text)
        return data['payload']['state']

    def setStateFor(self, socket_id: int, socket_state: bool) -> None:
        url = f"{self.apiURL}/socket/{socket_id}/{'on' if socket_state else 'off'}"
        response = requests.post(url, verify=self.ssl)

        if (response.status_code != 200):
            raise RuntimeError(
                f'Failed to update socket status: {response.status_code} ({response.text})'
            )

    def testConnection(self) -> bool:
        url = f"{self.apiURL}/ping"
        response = requests.get(url, verify=self.ssl)
        return response.status_code == 200

    def __init__(self, host: str, name: str = "", apiPort: int = 3000, metricsPort: int = 8000, certificate: str = ""):
        self.name = name
        self.host = host

        # API Server Configuration
        self.apiPort = apiPort
        self.certificate = certificate
        self.ssl = self.certificate if self.certificate != "" else False
        self.apiURL = f"{'http' if self.ssl == False else 'https'}://{self.host}:{self.apiPort}/api/v1"

        # Metrics Server Configuration
        self.metricsPort = metricsPort
        self.metricsURL = f"http://{self.host}:{self.metricsPort}"
