#!/usr/bin/python3

import argparse
import os
import sys
from importlib.metadata import version


def parse_args(sys_args):
    """ Parse Arguments for Cerberus

    Args:
        sys_args (sys.args): System arguments to parse

    Returns:
        argparse.Namespace: command line arguments
    """

    args = argparse.ArgumentParser(
        prog="cerberus",
        description="Proactive layer 2 Openflow Controller"
    )
    args.add_argument(
        '-c', '--config',
        action='store',
        help="Specify config file"
    )
    args.add_argument(
        '-v', '--version',
        action='store_true',
        help="Print version and exit"
    )
    args.add_argument(
        '--verbose',
        action='store_true',
        help='Enables verbose logging'
    )
    args.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Runs in background with no output'
    )
    ryu_args = args.add_argument_group('ryu-manager arguments')
    ryu_args.add_argument(
        '--wsapi-host',
        dest='wsapi_host',
        action='store',
        help="webapp listen host (default 0.0.0.0)"
    )
    ryu_args.add_argument(
        '--wsapi-port',
        dest='wsapi_port',
        action='store',
        help="webapp listen host (default 8080)"
    )
    ryu_args.add_argument(
        '--ofp-listen-host',
        dest='ofp_host',
        action='store',
        help="OpenFlow listen host (default 0.0.0.0)"
    )
    ryu_args.add_argument(
        '--ofp-ssl-listen-port',
        dest='ofp_ssl_port',
        action='store',
        help="OpenFlow SSL listen port (default 6653)"
    )
    ryu_args.add_argument(
        '--ofp-tcp-listen-port',
        dest='ofp_tcp_port',
        action='store',
        help="OpenFlow tcp listen port (default 6653)"
    )
    return args.parse_args(sys_args)


def print_version():
    print(f"Cerberus: {version('cerberus-controller')}")
    sys.exit()


def main():
    """ Main program launching point """
    args = parse_args(sys.argv[1:])

    if args.version:
        print_version()

    ryu_args = []
    if args.wsapi_host:
       ryu_args.extend(["--wsapi-host", args.wsapi_host])
    if args.wsapi_port:
        ryu_args.extend(["--wsapi-port", args.wsapi_port])
    if args.ofp_host:
        ryu_args.extend(["--ofp-listen-host", args.ofp_host])
    if args.ofp_tcp_port:
        ryu_args.extend(["--ofp-tcp-listen-port", args.ofp_tcp_port])
    if args.ofp_ssl_port:
        ryu_args.extend(["--ofp-ssl-listen-port", args.ofp_ssl_port])

    os.execvp('ryu-manager', ['ryu-manager', *ryu_args ,'cerberus.cerberus'])


if __name__ == '__main__':
    main()