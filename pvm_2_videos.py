from datetime import datetime
import os
from pythonosc import dispatcher, osc_server
import argparse
from omxplayer.player import OMXPlayer
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

def _init_logger():
	logger = logging.getLogger("PVM")
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stderr)
	fileHandler = TimedRotatingFileHandler('./log/{:%Y-%m-%d %H:%M:%S}.log'.format(datetime.now()),  when='midnight')
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
	fileHandler.setFormatter(formatter)
	fileHandler.suffix = '%Y_%m_%d.log'
	logger.addHandler(fileHandler)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

_init_logger()
_logger = logging.getLogger("PVM")
_logger.info("Logging system initilized in %s", os.getcwd())

# Place your videos in this folder for autostart
PEFIX_PATH = "/home/pi/Videos/"
VIDEO_PATH_ONE = "jellyfish720p.mp4"
VIDEO_PATH_TWO = "jellyfish720p.mp4"
media1 = ""
media2 = ""
IS_FILE_SET = False

def parse_commands(*args):
	global media1
	global media2
	global VIDEO_PATH_ONE
	global VIDEO_PATH_TWO
	global IS_FILE_SET
	command = args[1]
	_logger.info("Received command: %s", command)
	if len(args)>2:
		value = args[2]
		_logger.info("Received command: %s", str(value))
		pass
	# TODO: Create another python file to control two display
	if command=="file":
		if "|" not in value:
			_logger.info("Please pass two video name like 1.mp4,2.mp4.")
			return
		VIDEO_PATH_ONE, VIDEO_PATH_TWO = value.split("|")
		_logger.info("File set: %s, %s", PEFIX_PATH + VIDEO_PATH_ONE, PEFIX_PATH + VIDEO_PATH_TWO)
		IS_FILE_SET = True
		media1 = OMXPlayer(PEFIX_PATH + VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop', '--display', '2'])
		media1.pause()
		media2 = OMXPlayer(PEFIX_PATH + VIDEO_PATH_TWO, dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=['--loop', '--display', '7'])
		media2.pause()
		return

	if not IS_FILE_SET:
		_logger.info("Command %s failed because of the file is unset.", command)
		return

	if command=="start":
		if media1.can_play():
			# check two videos' position
			pos1=media1.position()
			pos2=media2.position()
			offset =abs(pos1-pos2)
			if(offset>1): #more than 1 second offset, direct jump to correct position
				media2.set_position(pos1)
			
			media1.play()
			media2.play()
			_logger.info("%s command success.", command)
		else:
			_logger.info("%s command failed.", command)
	elif command=="stop":
		if media1.can_quit():
			media1.quit()
			media2.quit()
			IS_FILE_SET = False
			_logger.info("%s command success and file has been unset.", command)
		else:
			_logger.info("%s command failed.", command)
	elif command=="set_position":
		media1.set_position(float(value))
		media2.set_position(float(value))
		_logger.info("%s command success.", command)
	elif command=="set_rate":
		fps = str(30 * float(value))
		media1 = OMXPlayer(PEFIX_PATH + VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop', '--display', '2', '--force-fps', fps])
		media1.pause()
		media2 = OMXPlayer(PEFIX_PATH + VIDEO_PATH_TWO, dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=['--loop', '--display', '7', '--force-fps', fps])
		media2.pause()
		_logger.info("%s command success.", command)
	elif command=="pause":
		if media1.can_pause():
			media1.pause()
			media2.pause()
			_logger.info("%s command success.", command)
		else:
			_logger.info("%s command failed.", command)
	else:
		_logger.info("%s unknown.", command)


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
