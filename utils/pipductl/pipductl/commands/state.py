from . import cli, servers
import click

@cli.command()
@click.option('--server', '-S', type=str, required=True, help='List sockets for a particular server')
@click.option('--socket', '-s', type=int, required=True, help='Set the state of a particular socket')
@click.argument('state', type=click.Choice(['on', 'off']))
def set_state(state, server, socket):
    if server not in servers:
        raise NameError(f"Unknown server {server}")
    servers.get(server).setStateFor(socket, state=="on")

@cli.command()
@click.option('--server', '-S', type=str, required=True, help='Get the state of sockets for a particular server')
@click.option('--socket', '-s', type=int, required=True, help='Get the state of a particular socket')
def get_state(server, socket):
    if server not in servers:
        raise NameError(f"Unknown server {server}")
    print(servers.get(server).getStateFor(socket))
