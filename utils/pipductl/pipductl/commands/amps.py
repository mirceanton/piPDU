from . import cli, servers
import click

def __validate_server_options(all_servers: bool | None, server: str | None, socket: int | None):
    if not server and not all_servers:
        raise click.UsageError('The -S/--server option is required when the -A/--all-servers option is not provided.')

    if socket and not server:
        raise click.UsageError('The -S/--server option is required when the -s/--socket option is used.')

@cli.command()
@click.option('--all-servers', '-A', is_flag=True, help='Show the total power consumption spanning all configured pipdu servers.')
@click.option('--server', '-S', type=str, help='Show the total power consumption for a given pipdu servers')
@click.option('--socket', '-s', type=int, help='Narrow down the power consumption to a single socket on a pipdu server')
def get_amps(all_servers, server, socket):
    __validate_server_options(all_servers, server, socket)

    if all_servers:
        for server in servers:
            print(f"{server}: {servers.get(server).getGlobalMetrics()}")
        return

    if socket is not None:
        print(servers.get(server).getMetricsFor(socket))
        return

    print(servers.get(server).getGlobalMetrics())
