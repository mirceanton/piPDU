from . import cli, servers

@cli.command()
def get_servers():
    for key,value in servers.items():
        print(f"{key}:")
        print(f"  host: {value.host}")
        print(f"  apiPort: {value.apiPort}")
        print(f"  metricsPort: {value.metricsPort}")
