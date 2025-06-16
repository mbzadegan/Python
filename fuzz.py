#!/usr/bin/env python3

import argparse
import random
import time
import sys
from scapy.all import *

def fuzz_tcp(target, count, delay):
    print(f"[+] Fuzzing TCP to {target} for {count} packets")
    for i in range(count):
        pkt = IP(dst=target, ttl=random.randint(1, 255), id=RandShort(), flags=0) / \
              TCP(sport=RandShort(), dport=random.choice([22, 80, 443]),
                  flags=random.choice(["S", "A", "F", "R", "SA", "FA"]),
                  window=RandShort()) / \
              Raw(load=RandString(random.randint(10, 100)))
        print(pkt.summary())
        send(pkt, verbose=False)
        time.sleep(delay)

def fuzz_udp(target, count, delay):
    print(f"[+] Fuzzing UDP to {target} for {count} packets")
    for i in range(count):
        pkt = IP(dst=target, ttl=random.randint(1, 255), id=RandShort(), flags=0) / \
              UDP(sport=RandShort(), dport=random.choice([53, 123, 161])) / \
              Raw(load=RandString(random.randint(10, 200)))
        print(pkt.summary())
        send(pkt, verbose=False)
        time.sleep(delay)

def fuzz_icmp(target, count, delay):
    print(f"[+] Fuzzing ICMP to {target} for {count} packets")
    for i in range(count):
        pkt = IP(dst=target, ttl=random.randint(1, 255), id=RandShort()) / \
              ICMP(type=random.choice([0, 3, 5, 8, 11, 13]), code=random.randint(0, 15)) / \
              Raw(load=RandString(random.randint(10, 100)))
        print(pkt.summary())
        send(pkt, verbose=False)
        time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description="Black-box packet fuzzer")
    parser.add_argument("--target", help="Target IP address")
    parser.add_argument("--proto", choices=["tcp", "udp", "icmp"], help="Protocol to fuzz")
    parser.add_argument("--count", type=int, default=100, help="Number of packets to send (default: 100)")
    parser.add_argument("--delay", type=float, default=0.01, help="Delay between packets (default: 0.01s)")

    # If no args are passed, print usage.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if not args.target or not args.proto:
        parser.print_help()
        sys.exit(1)

    if args.proto == "tcp":
        fuzz_tcp(args.target, args.count, args.delay)
    elif args.proto == "udp":
        fuzz_udp(args.target, args.count, args.delay)
    elif args.proto == "icmp":
        fuzz_icmp(args.target, args.count, args.delay)

if __name__ == "__main__":
    main()
