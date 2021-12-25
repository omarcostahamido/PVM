import os
import time
from subprocess import PIPE, Popen
from pythonosc import dispatcher, osc_server, udp_client
import socket
import argparse

cmd1 = "vlc jellyfish720p.mp4 -I rc"
cmd2 = b"loop\n"

p = Popen(cmd1.split(),stdin=PIPE)

p.stdin.write(cmd2)
p.stdin.flush()

def parse_commands(*args):
    # data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # data = data.decode('UTF-8').split()
    command = args[1]
    if len(args)>2:
    	value = args[2]
    	pass
    if command=="start":
    	# media.play()
    	p.stdin.write(b"play\n")
    	p.stdin.flush()
    	pass
    if command=="stop":
    	# media.stop()
    	p.stdin.write(b"stop\n")
		p.stdin.flush()
    	pass
    if command=="set_position":
    	# media.set_position(float(value))
    	cmd = b"seek \"%f\"" % float(value)
    	p.stdin.write(cmd)
		p.stdin.flush()
    	pass
    if command=="fullscreen":
    	# media.set_fullscreen(True)
    	# media.toggle_fullscreen()
    	p.stdin.write(b"fullscreen\n")
		p.stdin.flush()
    	pass
    if command=="set_rate":
    	# media.set_fullscreen(True)
    	# media.set_rate(float(value))
    	cmd = b"rate \"%f\"" % float(value)
    	p.stdin.write(cmd)
		p.stdin.flush()
    	pass
    if command=="pause":
    	# media.set_fullscreen(True)
    	# media.pause()
    	p.stdin.write(b"pause\n")
		p.stdin.flush()
    	pass
    if command=="next_frame":
    	# media.set_fullscreen(True)
    	# media.next_frame()
    	p.stdin.write(b"frame\n")
		p.stdin.flush()
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
    print('Omar Costa Hamido 2022')
    main(args.port)