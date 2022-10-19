from pythonosc import dispatcher, osc_server, udp_client
import socket
import argparse
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
media_log = logging.getLogger("Player 1")

VIDEO_PATH = "jellyfish720p.mp4"
media = ""


# media = vlc.MediaPlayer("jellyfish720p.mp4")

#media.set_fullscreen(True)

# media.play()

#media.stop()
# def parse_qasm(*args):
#     for arg in args:
#     	print(arg)

# while True:
def parse_commands(*args):
	global media
	global VIDEO_PATH
	command = args[1]
	print("command: "+command)
	if len(args)>2:
		value = args[2]
		print("value: "+str(value))
		pass
	if command=="file":
		media = OMXPlayer(value, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop'])
		media.pause()
		VIDEO_PATH = value
	elif command=="start":
		media.play()
	elif command=="stop":
		media.stop()
	elif command=="set_position":
		media.set_position(float(value))
	elif command=="set_rate":
		fps = str(30 * float(value))
		media = OMXPlayer(VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop','--force-fps', fps])
		media.pause()
	elif command=="pause":
		media.pause()
	else:
		print("I received command \"%s\" but I don't know what to do with it, yet." % command)


def main(RECEIVE_PORT):
	#OSC server
	# media = inst.media_player_new(FILE)
	callback = dispatcher.Dispatcher()
	server = osc_server.ThreadingOSCUDPServer(("", RECEIVE_PORT), callback)
	print("server now listenning on port "+str(RECEIVE_PORT))
	callback.map("/PVM", parse_commands)
	server.serve_forever()

if __name__ == '__main__':
	p = argparse.ArgumentParser()
	p.add_argument('--port', type=int, nargs='?', default=8001, help='The port that pvm.py will use to receive control messages. Default port is 8001')
	# p.add_argument('--file', nargs='?', default='jellyfish720p.mp4', help='The file that pvm.py will load. Default is jellyfish720p.mp4')
	args = p.parse_args()
	print('PVM - Pi Video Machine')
	print('Omar Costa Hamido 2022')
	main(args.port)


# UDP_IP = ""
# UDP_PORT = 8000 #add possibility to change this

# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.bind((UDP_IP, UDP_PORT))