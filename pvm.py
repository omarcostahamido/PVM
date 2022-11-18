from datetime import datetime, timedelta
import os
from pathlib import Path
from time import sleep
from pythonosc import dispatcher, osc_server
import argparse
from omxplayer.player import OMXPlayer
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

# Initialize global variables
HOME = str(Path.home()) + "/"  # The home directory, e.g. /home/pi/
LOG_PATH = HOME + "PVM/log/"
PEFIX_PATH = HOME + "Videos/" # Place your videos in this folder for autostart
VIDEO_PATH_ONE = "jellyfish720p.mp4"
VIDEO_PATH_TWO = "jellyfish720p.mp4"
media1 = None
media2 = None
IS_FILE_SET = False

"""
Initialize the log object
Output the system log to stderr and file at the Info level
"""

def _init_logger():
	global LOG_PATH
	logger = logging.getLogger("PVM")
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stderr)
	# Check if the `log` directory exists, create one if not.
	log_path = LOG_PATH + "{:%Y-%m-%d %H:%M:%S}.log"
	if not os.path.exists(log_path):
		os.makedirs(log_path)
	fileHandler = TimedRotatingFileHandler(log_path.format(datetime.now()),  when='midnight')
	LOG_PATH = log_path.format(datetime.now())
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s.%(msecs)03d;%(levelname)s;%(message)s",
							  "%Y-%m-%d %H:%M:%S")
	fileHandler.setFormatter(formatter)
	logger.addHandler(fileHandler)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

# Log system initiated
_init_logger()
_logger = logging.getLogger("PVM")
_logger.info("Logging system initiated in %s", LOG_PATH)

'''
UDP command example:
/PVM HH MM SS <command> <value>
'''

# Parse UDP command
def parse_commands(*args):
	global media1
	global media2
	global VIDEO_PATH_ONE
	global VIDEO_PATH_TWO
	global IS_FILE_SET
	global canPause
	global canStart
	global displayNum

	# Parse time and add 3 seconds
	hh, mm, ss = args[1], args[2], args[3]
	time_str = str(hh) + ":" + str(mm) + ":" + str(ss)
	next_time = datetime.strptime(time_str, "%H:%M:%S") + timedelta(seconds=3)

	# Get command
	command = args[4]

	# If scheduled time is behind current time, return.
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
	if len(args) == 6:
		value = args[5]

	# Catch failed parse command
	try:
		# File command
		if command=="file":
			# define displayNum here
			if "|" not in value:
				displayNum = 1
			else:
				displayNum = 2

			if displayNum == 1:
				VIDEO_PATH_ONE = PEFIX_PATH + value
				_logger.info("File set: %s with 1 video output.", VIDEO_PATH_ONE)
				if IS_FILE_SET:
					_logger.info("The file has already been set, please hit stop first.")
					return
				# Change flags
				IS_FILE_SET = True
				canStart = True
				canPause = False
				media1 = OMXPlayer(VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop'])
				media1.pause()
			else:
				VIDEO_PATH_ONE, VIDEO_PATH_TWO = parse_value(value)
				VIDEO_PATH_ONE = PEFIX_PATH + VIDEO_PATH_ONE
				VIDEO_PATH_TWO = PEFIX_PATH + VIDEO_PATH_TWO
				_logger.info("File set: %s, %s with 2 video outputs.", VIDEO_PATH_ONE, VIDEO_PATH_TWO)
				if IS_FILE_SET:
					_logger.info("The files have already been set, please hit stop first.")
					return
				# Change flags
				IS_FILE_SET = True
				canStart = True
				canPause = False
				media1 = OMXPlayer(VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop', '--display', '2'])
				media1.pause()
				media2 = OMXPlayer(VIDEO_PATH_TWO, dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=['--loop', '--display', '7'])
				media2.pause()
			return

		# If file is unset, then we should not execute any command below.
		if not IS_FILE_SET:
			_logger.info("Command %s failed because of the file is unset.", command)
			return

		# If Raspberry Pi has two displays.
		if displayNum == 2:
			if command=="start":
				if canStart:
						# Get position for media1 and media2
						pos1 = media1.position()
						pos2 = media2.position()
						# Always set position for the fast media to slow one.
						if pos1 > pos2:
							media1.set_position(pos2)
						elif pos1 < pos2:
							media2.set_position(pos1)		
						pos1 = media1.position()
						_logger.info("media 1&2 position: %s", pos1)
						# Play both media
						media1.play()
						media2.play()
						# Change canPause and canStart
						canPause = True
						canStart = False
						_logger.info("%s command success.", command)
				else:
					_logger.info("%s command failed.", command)
			elif command=="stop":
				if media1.can_quit():
					media1.quit()
					media2.quit()
					IS_FILE_SET = False
					canPause = False
					canStart = False
					_logger.info("%s command success and file has been unset.", command)
				else:
					_logger.info("%s command failed.", command)
			elif command=="set_position":
				media1.set_position(float(value))
				media2.set_position(float(value))
				_logger.info("%s command success.", command)
			elif command=="set_rate":
				v1, v2 = parse_value(value)
				fps1 = get_rate(VIDEO_PATH_ONE, v1)
				fps2 = get_rate(VIDEO_PATH_ONE, v2)
				media1 = OMXPlayer(VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop', '--display', '2', '--force-fps', fps1])
				media1.pause()
				media2 = OMXPlayer(VIDEO_PATH_TWO, dbus_name='org.mpris.MediaPlayer2.omxplayer2', args=['--loop', '--display', '7', '--force-fps', fps2])
				media2.pause()
				_logger.info("%s command success.", command)
			elif command=="pause":
				if canPause:
						media1.pause()
						media2.pause()
						pos1 = media1.position()
						pos2 = media2.position()
						_logger.info("media 1 position: %s", pos1)
						_logger.info("media 2 position: %s", pos2)
						if pos1 > pos2:
							media1.set_position(pos2)
							_logger.info("media 1 set position: %s", pos2)
						elif pos1 < pos2:
							media2.set_position(pos1)
							_logger.info("media 2 set position: %s", pos1)
						canPause = False
						canStart = True
						_logger.info("%s command success.", command)
			else:
				_logger.info("%s unknown.", command)
		else:
			# If Raspberry Pi only has one display.
			if command=="start":
				if canStart:							
						media1.play()
						canPause = True
						canStart = False
						_logger.info("%s command success.", command)
				else:
					_logger.info("%s command failed.", command)
			elif command=="stop":
				if media1.can_quit():
					media1.quit()
					IS_FILE_SET = False
					canStart = False
					canPause = False
					_logger.info("%s command success and file has been unset.", command)
				else:
					_logger.info("%s command failed.", command)
			elif command=="set_position":
				media1.set_position(float(value))
				_logger.info("%s command success.", command)
			elif command=="set_rate":
				fps = get_rate(VIDEO_PATH_ONE, value)
				media1 = OMXPlayer(VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop', '--force-fps', fps])
				media1.pause()
				canStart = True
				canPause = False
				_logger.info("%s command success.", command)
			elif command=="pause":
				if canPause:
						media1.pause()
						canPause = False
						canStart = True
						_logger.info("%s command success.", command)
				else:
					_logger.info("%s command failed.", command)
			else:
				_logger.info("%s unknown.", command)
	except Exception as e:
		# `logger#exception method prints the stack trace`
		_logger.exception("Function: parse_commands failed! %s" % (e))

# get fps from video path
def get_rate(path, value):
	media = OMXPlayer(VIDEO_PATH_ONE, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop','--force-fps', fps])
	video_info = subprocess.Popen(["omxplayer", "-i", VIDEO_PATH_ONE], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	out, err = video_info.communicate()
	out = out.decode(encoding='utf-8')
	splist = out.split(", ")
	for s in splist:
		if 'fps' in s:
			fps_info = s.split(' ')
			original_fps = float(fps_info[0])
	fps = str(original_fps * float(value))

def parse_value(value):
	value1, value2 = value.split("|")
	if value1 is None or value2 == '':
		value2 = value1
	return value1, value2

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
