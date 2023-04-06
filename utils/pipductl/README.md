# `pipductl` - A Command-Line Utility for Managing PiPDU Devices

`pipductl` is a command-line utility that provides a simple interface for controlling PiPDU devices. With `pipductl`, you can turn individual sockets on or off, view the current state of each socket, and retrieve power usage metrics.

## Installation

To use `pipductl`, you will need to have Python 3.7 or later installed on your system. You can then install `pipductl` and its dependencies using pip:

```bash
pip install pipductl
```

## Usage

Once you have installed `pipductl`, you can use it from the command line by running the `pipductl` command:

```bash
pipductl <command> [<args>]
```

`pipductl` supports the following commands:

- `get-servers`: List all configured PDUs and their configuration.
- `set-state`: Set the state (`on`/`off`) of a specific socket on a specific PDU.
- `get-state`: Get the current state (`on`/`off`) of a specific socket on a specific PDU.
- `get-amps`: Get the current power usage for a specific socket on a specific PDU, for all sockets on a specific PDU or for all PDUs in aggregate.

For more information on each command and its options, run `pipductl <command> --help`.

## Configuration

TODO

## License

pipductl is released under the MIT license. See LICENSE.txt for more information.