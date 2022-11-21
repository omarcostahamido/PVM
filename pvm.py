from datetime import datetime, timedelta
import os
from pathlib import Path
import subprocess
from time import sleep
from pythonosc import dispatcher, osc_server
import argparse
from omxplayer.player import OMXPlayer
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

'''
Global variables used in the program
'''
HOME = str(Path.home()) + "/"  # The home directory, e.g. /home/pi/
LOG_PATH = HOME + "PVM/log/" # Log path
PREFIX_VIDEOS_PATH = HOME + "Videos/" # Place your videos in this folder for autostart
VIDEO_PATH = None # Video path
OMX = None	# OMXPlayer object
IS_FILE_SET = False # File set flag
CAN_PAUSE = False # Can pause flag
CAN_START = False # Can start flag

'''
UDP command example:
/PVM HH MM SS <command> <value>
'''
def parse_commands(*args):
	global OMX
	global PREFIX_VIDEOS_PATH
	global VIDEO_PATH
	global IS_FILE_SET
	global CAN_START
	global CAN_PAUSE
	global PORT

	# Get command
	command = args[4]
	
	# Only start and pause command need to delay 3s
	if command == "start" or command == "pause" or command == "set_rate":
		# Parse time and add 3 seconds
		hh, mm, ss = args[1], args[2], args[3]
		time_str = str(hh) + ":" + str(mm) + ":" + str(ss)
		next_time = datetime.strptime(time_str, "%H:%M:%S") + timedelta(seconds=3)

		# If scheduled time is behind current time, return.
		# In very rare cases, the control computer will have a three-second time difference with the Raspberry Pi
		if next_time.time() <= datetime.now().time():
			_logger.info("Command: %s failed because scheduled time(%s) is behind current time.", command, time_str)
			return

		# Log command and execute time.
		_logger.info("Command: %s, execute time: %s.", command, next_time.time())
		
		# Wait until current time is equal to next_time
		while True:
			now = datetime.now()
			now = now.replace(microsecond=0)
			if now.time() >= next_time.time():
				break
			sleep(0.005)

	# Get value
	if len(args) >= 6:
		value = args[5]

	# If PORT == 8001, we export our video in the main display 2,
	# else we export our video on the extra display 7
	params = ['--loop', '--display']
	if PORT == 8001:
		params.append('2')
	else:
		params.append('7')

	# Catch the excpetion if Dbus is down.
	try:
		# File command
		if command == "file":
			# If the file is already set, we exit OMX first
			if IS_FILE_SET:
				OMX.quit()
				_logger.info("Quit previous file: %s", VIDEO_PATH)
				IS_FILE_SET = False
			VIDEO_PATH = PREFIX_VIDEOS_PATH + value
			if PORT == 8001:
				OMX = OMXPlayer(VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=params)
			else:
				OMX = OMXPlayer(VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=params)	
			# Because OMX has no user interface and will play automatically once the OMXPlayer object is created, 
			# we need to call the puase() method after it is created.
			OMX.pause()
			IS_FILE_SET = True
			CAN_START = True
			CAN_PAUSE = False
			_logger.info("File set: %s. You can start now!", VIDEO_PATH)
			return

		# If file is unset, then we should not execute any command below.
		if not IS_FILE_SET:
			_logger.info("Command %s failed because of the file is unset.", command)
			return

		if command == "start":
			if CAN_START:
				OMX.play()
				CAN_START = False
				CAN_PAUSE = True
				_logger.info("%s command success.", command)
			else:
				_logger.info("%s command failed.", command)
		elif command == "pause":
			if CAN_PAUSE:
				OMX.pause()
				CAN_PAUSE = False
				CAN_START = True
				_logger.info("%s command success.", command)
			else:
				_logger.info("%s command failed.", command)
		elif command == "stop":
			OMX.stop()
			IS_FILE_SET = False
			CAN_START = False
			CAN_PAUSE = False
			_logger.info("%s command success and %s has been unset.", command, VIDEO_PATH)
		elif command == "set_position":
			OMX.set_position(float(value))
			_logger.info("%s command success.", command)
		elif command == "set_frame":
			fps, _ = get_info()
			frame_pos = 1.0 / fps * float(value)
			OMX.set_position(frame_pos)
			_logger.info("%s command success.", command)
		elif command == "relative_set_position":
			_, total_seconds = get_info()
			relative_pos = total_seconds / float(value)
			OMX.set_position(relative_pos)
			_logger.info("%s command success.", command)
		elif command == "set_rate":
			OMX.set_rate(float(value))
			_logger.info("%s command success set rate: %s.", command, value)
		else:
			_logger.info("%s unknown.", command)
	except Exception as e:
		# `logger#exception method prints the stack trace`
		_logger.exception("Function: parse_commands failed! %s" % (e))

# Get info from video path
# Return fps, total_seconds
def get_info():
	global VIDEO_PATH
	video_info = subprocess.Popen(["omxplayer", "-i", VIDEO_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	out, _ = video_info.communicate()
	out = out.decode(encoding='utf-8')
	splist = out.split(", ")
	for s in splist:
		if 'fps' in s:
			fps_info = s.split(' ')
			fps = float(fps_info[0])
		if 'Duration:' in s:
			duration_str = s.split('Duration: ')[1]
			pt = datetime.strptime(duration_str, "%H:%M:%S.%f")
			total_seconds = pt.second + pt.minute*60 + pt.hour*3600 + pt.microsecond / 1000
	return fps, total_seconds

# Output INFO-level logs to stderr and file
def _init_logger():
	global LOG_PATH
	global PORT
	logger = logging.getLogger("PVM")
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stderr)
	# Check if the `log` directory exists, create one if not.
	log_path = LOG_PATH + "{:%Y-%m-%d %H:%M:%S}-" + str(PORT) + ".log"
	if not os.path.exists(LOG_PATH):
		os.makedirs(LOG_PATH)
	fileHandler = TimedRotatingFileHandler(log_path.format(datetime.now()),  when='midnight')
	LOG_PATH = log_path.format(datetime.now())
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s.%(msecs)03d;%(levelname)s;" + str(PORT) + ";%(message)s",
							  "%Y-%m-%d %H:%M:%S")
	fileHandler.setFormatter(formatter)
	logger.addHandler(fileHandler)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

def main(RECEIVE_PORT):
	#OSC server
	callback = dispatcher.Dispatcher()
	server = osc_server.ThreadingOSCUDPServer(("", RECEIVE_PORT), callback)
	_logger.info("Server now listenning on port "+str(RECEIVE_PORT))
	callback.map("/PVM", parse_commands)
	server.serve_forever()

if __name__ == '__main__':
	global PORT
	global _logger
	p = argparse.ArgumentParser()
	p.add_argument('--port', type=int, nargs='?', default=8001, help='The port that pvm.py will use to receive control messages. Default port is 8001')
	args = p.parse_args()
	PORT = args.port
	_init_logger()
	_logger = logging.getLogger("PVM")
	_logger.info("Logging system initiated")
	_logger.info("PVM - Pi Video Machine")
	_logger.info("Omar Costa Hamido 2022")
	main(PORT)
