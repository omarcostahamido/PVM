from datetime import datetime
import os
from time import sleep
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
	formatter = logging.Formatter("%(asctime)s.%(msecs)03d;%(levelname)s;%(message)s",
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
VIDEO_PATH = "jellyfish720p.mp4"
media = ""
IS_FILE_SET = False
NEXT_TIME = None

'''
UDP command example:
/PVM 12:13:14
/PVM <action_name> <action_value>

The normal workflow is below,
1. Receive the first command: /PVM 12:13:14
	- parse the time
	- plus 3s
	- save the time into NEXT_TIME
2. Receive the second command: /PVM file jellyfish.mp4
	- Wait until the NEXT_TIME
	- Execute the command
	- Set NEXT_TIME = None
'''

def parse_commands(*args):
	global media
	global VIDEO_PATH
	global IS_FILE_SET
	global NEXT_TIME
	# Parse the time send in UDP, 
	# From /PVM 12 13 14 to 12:13:14
	if len(args) == 4:
		seconds = int(args[3]) + 3
		minutes = int(args[2])
		hours = int(args[1])
		if seconds >= 60:
			seconds -= 60
			minutes += 1
		if minutes == 60:
			minutes = 0
			hours += 1
		time_data = str(hours) + ":" + str(minutes) + ":" + str(seconds)
		# Set NEXT_TIME for next UDP command
		NEXT_TIME = datetime.strptime(time_data, "%H:%M:%S")
		# If scheduled time is behind current time, we set NEXT_TIME = None
		if NEXT_TIME.time <= datetime.now().time():
			_logger.info("Timestamp set failed.")
			NEXT_TIME = None
			return
		_logger.info("Next action will be done in %s", time_data)
		return
	
	# UDP Command example: /PVM <action_name> <action_value>
	command = args[1]
	# If NEXT_TIME is None, we log failed and return.
	if not NEXT_TIME:
		_logger.info("Action: %s failed because scheduled time is behind current time.", command)
		return
	
	# Received command here and will try to execute.
	_logger.info("Received command: %s", command)
	if len(args)>2:
		value = args[2]
		_logger.info("Received value: %s", str(value))
		pass
	
	# Loop until now.time() >= NEXT_TIME.time()
	# Here is the logic of our delay
	while True:
		now = datetime.now()
		now = now.replace(microsecond=0)
		if now.time() >= NEXT_TIME.time():
			break
		sleep(0.01)
	
	# File command
	if command=="file":
		_logger.info("File set: %s", PEFIX_PATH + value)
		IS_FILE_SET = True
		media = OMXPlayer(PEFIX_PATH + value, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop'])
		media.pause()
		VIDEO_PATH = value
		NEXT_TIME = None
		return

	# If file is unset, then we should not execute any command below.
	if not IS_FILE_SET:
		_logger.info("Command %s failed because of the file is unset.", command)
		NEXT_TIME = None
		return

	if command=="start":
		if media.can_play():
			media.play()
			_logger.info("%s command success.", command)
		else:
			_logger.info("%s command failed.", command)
	elif command=="stop":
		if media.can_quit():
			media.stop()
			IS_FILE_SET = False
			_logger.info("%s command success and file has been unset.", command)
		else:
			_logger.info("%s command failed.", command)
	elif command=="set_position":
		media.set_position(float(value))
		_logger.info("%s command success.", command)
	elif command=="set_rate":
		fps = str(30 * float(value))
		media = OMXPlayer(PEFIX_PATH + VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop','--force-fps', fps])
		media.pause()
		_logger.info("%s command success.", command)
	elif command=="pause":
		if media.can_pause():
			media.pause()
			_logger.info("%s command success.", command)
		else:
			_logger.info("%s command failed.", command)
	else:
		_logger.info("%s unknown.", command)
	
	# To set NEXT_TIME = None, so that it will not confuse next command.
	NEXT_TIME = None


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
