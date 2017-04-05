## Multicast Receive


from socket import *
import struct

MCAST_GRP = '0.0.0.0'
MCAST_PORT = 5007

sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)

sock.bind((MCAST_GRP, MCAST_PORT))
print(INADDR_ANY)
## Use MCAST_GRP instead of '' to listen only to MCAST_GRP

mreq = struct.pack('4sl', inet_aton(MCAST_GRP), INADDR_ANY)

sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

while True:
	print sock.recv(1024)


