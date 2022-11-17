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
	# Check if the `log` directory exists, create one if not.
	log_path = "/home/pi/PVM/log/{:%Y-%m-%d %H:%M:%S}.log"
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

# Place your videos in this folder for autostart
LOG_PATH = "/home/pi/PVM/log/"
PEFIX_PATH = "/home/pi/Videos/"
VIDEO_PATH = "jellyfish720p.mp4"
media = ""
IS_FILE_SET = False

def parse_commands(*args):
	global media
	global VIDEO_PATH
	global IS_FILE_SET
	command = args[1]
	_logger.info("Received command: %s", command)
	if len(args)>2:
		value = args[2]
		_logger.info("Received command: %s", str(value))
		pass
	# TODO: Create another python file to control two display
	try:
		if command=="file":
			_logger.info("File set: %s", PEFIX_PATH + value)
			IS_FILE_SET = True
			media = OMXPlayer(PEFIX_PATH + value, dbus_name='org.mpris.MediaPlayer2.omxplayer', args=['--loop'])
			media.pause()
			VIDEO_PATH = value
			return

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
			media = OMXPlayer(PEFIX_PATH + VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer1', args=['--loop','--force-fps', fps])
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
