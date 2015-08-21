"""
Reads in .dump files and interprets them
"""
import argparse
import json
import sys
import os

def main():
    """
    Reads the dump files and runs the analysis
    """
    if os.path.exists("packet_dumps"):
        for fname in os.listdir("packet_dumps"):
            if any(fname.startswith(x) for x in args.protocols):
                with open("packet_dumps/%s" % fname) as f:
                    dump = json.load(f)
                    print "%s total transferred %s bytes" % (fname, sum_all(dump))
                    print "%s outgoing transferred %s bytes" % (fname, sum_outgoing(dump))

def sum_all(dump):
    """
    Returns the total bytes transferred between two hosts
    """
    return sum(int(l["length"]) for l in dump)

def sum_outgoing(dump):
    """
    Returns the total outgoing bytes of the transfer
    """
    return sum(int(l["length"]) for l in dump if l["direction"] == "outgoing")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--protocols", metavar="PROTOCOL", nargs="+",
                        default=["ftp", "scp", "gridftp"],
                        help="Can be any combination of gridftp, scp, ftp")
    args = parser.parse_args()

    sys.exit(main())
