import click
import pipdu_sdk


servers = pipdu_sdk.config.parse_yaml_config('config.yml')

@click.group()
def pipductl():
    pass

@pipductl.command()
def get_servers():
    for key,value in servers.items():
        print(f"{key}:")
        print(f"  host: {value.host}")
        print(f"  apiPort: {value.apiPort}")
        print(f"  metricsPort: {value.metricsPort}")

@pipductl.command()
@click.option('--server', '-S', type=str, required=True, help='List sockets for a particular server')
@click.option('--socket', '-s', type=int, required=True, help='Set the state of a particular socket')
@click.argument('state', type=click.Choice(['on', 'off']))
def set_state(state, server, socket):
    if server not in servers:
        raise NameError(f"Unknown server {server}")
    servers.get(server).setStateFor(socket, state=="on")

@pipductl.command()
@click.option('--server', '-S', type=str, required=True, help='Get the state of sockets for a particular server')
@click.option('--socket', '-s', type=int, required=True, help='Get the state of a particular socket')
def get_state(server, socket):
    if server not in servers:
        raise NameError(f"Unknown server {server}")
    print(servers.get(server).getStateFor(socket))

def validate_server_options(all_servers: bool | None, server: str | None, socket: int | None):
    if not server and not all_servers:
        raise click.UsageError('The -S/--server option is required when the -A/--all-servers option is not provided.')

    if socket and not server:
        raise click.UsageError('The -S/--server option is required when the -s/--socket option is used.')

@pipductl.command()
@click.option('--all-servers', '-A', is_flag=True, help='Show the total power consumption spanning all configured pipdu servers.')
@click.option('--server', '-S', type=str, help='Show the total power consumption for a given pipdu servers')
@click.option('--socket', '-s', type=int, help='Narrow down the power consumption to a single socket on a pipdu server')
def get_amps(all_servers, server, socket):
    validate_server_options(all_servers, server, socket)

    if all_servers:
        for server in servers:
            print(f"{server}: {servers.get(server).getGlobalMetrics()}")
        return

    if socket is not None:
        print(servers.get(server).getMetricsFor(socket))
        return

    print(servers.get(server).getGlobalMetrics())

pipductl()
