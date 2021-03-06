import os
import time
from subprocess import PIPE, Popen
from pythonosc import dispatcher, osc_server, udp_client
import socket
import argparse

cmd1 = "vlc zoetrope.mp4 -I rc"
cmd2 = b"loop\n"

proc = Popen(cmd1.split(),stdin=PIPE)

proc.stdin.write(cmd2)
proc.stdin.flush()

def parse_commands(*args):
    # data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # data = data.decode('UTF-8').split()
    command = args[1]
    if len(args)>2:
    	value = args[2]
    	pass
    if command=="start":
    	# media.play()
    	proc.stdin.write(b"play\n")
    	proc.stdin.flush()
    	pass
    if command=="stop":
    	# media.stop()
    	proc.stdin.write(b"stop\n")
    	proc.stdin.flush()
    	pass
    if command=="set_position":
    	# media.set_position(float(value))
    	cmd = b"seek \"%f\"" % float(value)
    	proc.stdin.write(cmd)
    	proc.stdin.flush()
    	pass
    if command=="fullscreen":
    	# media.set_fullscreen(True)
    	# media.toggle_fullscreen()
    	proc.stdin.write(b"fullscreen\n")
    	proc.stdin.flush()
    	pass
    if command=="set_rate":
    	# media.set_fullscreen(True)
    	# media.set_rate(float(value))
    	cmd = b"rate \"%f\"" % float(value)
    	proc.stdin.write(cmd)
    	proc.stdin.flush()
    	pass
    if command=="pause":
    	# media.set_fullscreen(True)
    	# media.pause()
    	proc.stdin.write(b"pause\n")
    	proc.stdin.flush()
    	pass
    if command=="next_frame":
    	# media.set_fullscreen(True)
    	# media.next_frame()
    	proc.stdin.write(b"frame\n")
    	proc.stdin.flush()
    	pass
    else:
    	print("I received command \"%s\" but I don't know what to do with it, yet." % command)


def main(RECEIVE_PORT):
    #OSC server
    # media = inst.media_player_new(FILE)
    callback = dispatcher.Dispatcher()
    server = osc_server.ThreadingOSCUDPServer(("", RECEIVE_PORT), callback)
    callback.map("/PVM", parse_commands)
    server.serve_forever()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, nargs='?', default=8001, help='The port that pvm.py will use to receive control messages. Default port is 8001')
    # p.add_argument('--file', nargs='?', default='jellyfish720p.mp4', help='The file that pvm.py will load. Default is jellyfish720p.mp4')
    args = p.parse_args()
    print('PVM - Pi Video Machine')
    print('alt version: vlc -I rc')
    print('Omar Costa Hamido 2022')
    main(args.port)