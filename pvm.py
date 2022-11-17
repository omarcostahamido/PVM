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

# Place your videos in this folder for autostart
HOME = str(Path.home()) + "/"  # The home directory, e.g. /home/pi/
LOG_PATH = HOME + "PVM/log/"
PREFIX_PATH = HOME + "Videos/"
VIDEO_PATH = "jellyfish720p.mp4"
IS_FILE_SET = False

def _init_logger():
	logger = logging.getLogger("PVM")
	logger.setLevel(logging.INFO)
	handler = logging.StreamHandler(sys.stderr)
	# Check if the `log` directory exists, create one if not.
	log_path = LOG_PATH + "{:%Y-%m-%d %H:%M:%S}.log"
	if not os.path.exists(log_path):
		os.makedirs(log_path)
	fileHandler = TimedRotatingFileHandler(log_path.format(datetime.now()),  when='midnight')
	global LOG_PATH
	LOG_PATH = log_path.format(datetime.now())
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter("%(asctime)s.%(msecs)03d;%(levelname)s;%(message)s",
							  "%Y-%m-%d %H:%M:%S")
	fileHandler.setFormatter(formatter)
	logger.addHandler(fileHandler)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

_init_logger()
_logger = logging.getLogger("PVM")
_logger.info("Logging system initiated in %s", LOG_PATH)

media = ""

'''
UDP command example:
/PVM HH MM SS <command> <value>
'''

def parse_commands(*args):
	global media
	global VIDEO_PATH
	global IS_FILE_SET
	
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

	try:
		# File command
		if command=="file":
			_logger.info("File set: %s", PREFIX_PATH + value)
			IS_FILE_SET = True
			media = OMXPlayer(PREFIX_PATH + value, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop'])
			media.pause()
			VIDEO_PATH = value
			return

		# If file is unset, then we should not execute any command below.
		if not IS_FILE_SET:
			_logger.info("Command %s failed because of the file is unset.", command)
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
			media = OMXPlayer(PREFIX_PATH + VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop','--force-fps', fps])
			if media != "":
				media.quit()
				print("media quit")
			original_fps = 30
			video_info = subprocess.Popen(["omxplayer", "-i", PEFIX_PATH + VIDEO_PATH], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			print("The command", ["omxplayer", "-i", PEFIX_PATH + VIDEO_PATH])
			# info = video_info.stdout.decode().split(", ")
			out, err = video_info.communicate()
			out = out.decode(encoding='utf-8')
			splist = out.split(", ")
			for s in splist:
				if 'fps' in s:
					print("current ele:", s)
					fps_info = s.split(' ')
					original_fps = float(fps_info[0])
			fps = str(original_fps * float(value))
			print("computed fps", fps)
			media = OMXPlayer(PREFIX_PATH + VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop','--force-fps', fps])
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
	except Exception as e:
		# `logger#exception method prints the stack trace`
		_logger.exception("Function: parse_commands failed! %s" % (e))

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
