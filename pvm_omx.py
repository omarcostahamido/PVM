from pythonosc import dispatcher, osc_server
import argparse
from omxplayer.player import OMXPlayer
import logging
import sys

def _init_logger():
	logger = logging.getLogger('PVM')
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stderr)
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
	handler.setFormatter(formatter)
	logger.addHandler(handler)

_init_logger()
_logger = logging.getLogger('PVM')
_logger.info("Logging system initilized!")
# logging example:
# _logger.info('App started in %s', os.getcwd())
# _logger.debug('App started in %s', os.getcwd())

VIDEO_PATH = "jellyfish720p.mp4"
# TODO: rename the variable
media = ""

# TODO: rewrite logging
# TODO: rewrite logic between commands
def parse_commands(*args):
	global media
	global VIDEO_PATH
	command = args[1]
	_logger.info("Command: %s", command)
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
	callback = dispatcher.Dispatcher()
	server = osc_server.ThreadingOSCUDPServer(("", RECEIVE_PORT), callback)
	print("server now listenning on port "+str(RECEIVE_PORT))
	callback.map("/PVM", parse_commands)
	server.serve_forever()

if __name__ == '__main__':
	p = argparse.ArgumentParser()
	p.add_argument('--port', type=int, nargs='?', default=8001, help='The port that pvm.py will use to receive control messages. Default port is 8001')
	args = p.parse_args()
	print('PVM - Pi Video Machine')
	print('Omar Costa Hamido 2022')
	main(args.port)


# UDP_IP = ""
# UDP_PORT = 8000 #add possibility to change this

# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.bind((UDP_IP, UDP_PORT))