#!/usr/bin/env python
from socket import *

MCAST_GRP = '0.0.0.0'
MCAST_PORT = 5007

sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 32)
sock.sendto("robot", (MCAST_GRP, MCAST_PORT))
