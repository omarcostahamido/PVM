from pythonosc import dispatcher, osc_server, udp_client
import random
import argparse
from pynput import keyboard
import socket

global ips, port

# def main(UDP_IP, SEND_PORT):
#     # if UDP_IP=="localhost":
#     #     UDP_IP="127.0.0.1"
#     #     pass

#     #OSC client
#     for ip in UDP_IP:
#     	print(ip)
# 	    client = udp_client.SimpleUDPClient(ip, SEND_PORT)

# if __name__ == '__main__':
#     p = argparse.ArgumentParser()
#     p.add_argument('--ip', nargs='*', help='The IP address(es) where the raspberry pi client(s) is/are located.')
#     p.add_argument('--port', nargs='*', default=8001, help='The port(s) that pvm.py initiated on the raspberry pi will use to receive control messages. Default port is 8001')

#     args = p.parse_args()

#     print('PVM - Pi Video Machine')
#     print('Omar Costa Hamido 2022')
#     # main(args.ip, args.port)
#     ips = args.ip
#     port = args.port

def on_press(key):
    try:
        if key.char == 's':
        	print("we pressed S!")
        	for ip in UDP_IP:
        		# client = udp_client.SimpleUDPClient(ip, port)
        		# client.send_message("/PVM", random.random())
        		MESSAGE = b"something else" 
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.sendto(MESSAGE, (ip, UDP_PORT))
        	pass
        if key.char=='j':
        	print("we pressed J!")
        	for ip in UDP_IP:
        		MESSAGE = b"john" 
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				sock.sendto(MESSAGE, (ip, UDP_PORT))
        		pass
        	pass
        # print('alphanumeric key {0} pressed'.format(
        #     key.char))
    except AttributeError:
        pass
        # print('special key {0} pressed'.format(
        #     key))

with keyboard.Listener(
        on_press=on_press) as listener:
	listener.join()


# def parse_qasm(*args):
#     # client.send_message("/PVM", random.random())
#     for arg in args:
#     	print(arg)



UDP_IP = "192.168.1.103"
UDP_PORT = 8000
MESSAGE = b"Hello, World!" 
# print("UDP target IP: %s" % UDP_IP)
# print("UDP target port: %s" % UDP_PORT)
# print("message: %s" % MESSAGE) 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))