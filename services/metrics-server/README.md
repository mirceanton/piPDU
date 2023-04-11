# PiPDU Metrics Server

## Configuration File

```yaml
apiVersion: v1.0.0
kind: MetricsConfig
data:
  server:
    port: 8000

  pollingIntervalSeconds: 0.1

  serial:
    device: /dev/ttyUSB0
    baud: 9600

  sensors:
    - pin: A0
    - pin: A1
```