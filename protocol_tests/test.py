"""
Gets information on packets transferred during a globus-url-copy
"""
import argparse
from datetime import datetime
import json
import os
import socket
import sys

from tcpdump import TcpDump
from protocols import PROC_ARGS, Protocol, get_ip_address

def main():
    """
    Do a transfer and log the packet data
    """
    for protocol in PROC_ARGS:
        test(protocol)

def test(protocol):
    """
    Takes a Protocol object and runs a test for it
    Outputs the dump to a file
    """
    protocol_obj = Protocol(args.host, args.remote_path, args.local_path, protocol)

    remote_hostname = args.host
    if "@" in remote_hostname:
        remote_hostname = remote_hostname[remote_hostname.find("@")+1:]

    remote_ip = socket.gethostbyname(remote_hostname)
    local_ip = get_ip_address(args.interface)
    dump = TcpDump(args.interface, remote_ip, local_ip)

    dump.start()
    protocol_obj.run()
    dump.stop()

    datestring = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    protocol_name = protocol_obj.protocol

    # Make sure the log directory exists
    if not os.path.exists("packet_dumps"):
        os.makedirs("packet_dumps")

    with open("packet_dumps/%s_%s.dump" % (protocol_name, datestring), "w") as f:
        json.dump(dump.output, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", metavar="INTERFACE", required=True,
                        help="The interface to capture packets on")
    parser.add_argument("-H", "--host", metavar="HOST", required=True,
                        help="The host which has the file to be copied")
    parser.add_argument("-r", "--remote-path", metavar="PATH", required=True,
                        help="The path of the file to be copied")
    parser.add_argument("-l", "--local-path", metavar="PATH", required=True,
                        help="The path where the file shold be copied to")
    args = parser.parse_args()

    sys.exit(main())
