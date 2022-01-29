import vlc
from pythonosc import dispatcher, osc_server, udp_client
import socket
import argparse

inst = vlc.Instance('--input-repeat=65535','--video-x=100')
media = inst.media_player_new("zoetrope.mp4")
# media = vlc.MediaPlayer("jellyfish720p.mp4")

#media.set_fullscreen(True)

# media.play()

#media.stop()
# def parse_qasm(*args):
#     for arg in args:
#     	print(arg)

# while True:
def parse_commands(*args):
	# data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	# data = data.decode('UTF-8').split()
	command = args[1]
	print("command: "+command)
	if len(args)>2:
    	value = args[2]
		print("value: "+value)
		pass
	if command=="file":
		print(value)
		media = inst.media_player_new(value)
		pass
	if command=="start":
		media.play()
		pass
	if command=="stop":
		media.stop()
		pass
	if command=="set_position":
		media.set_position(float(value))
		pass
	if command=="fullscreen":
		# media.set_fullscreen(True)
		media.toggle_fullscreen()
		pass
	if command=="set_rate":
		# media.set_fullscreen(True)
		media.set_rate(float(value))
		pass
	if command=="pause":
		# media.set_fullscreen(True)
		media.pause()
		pass
	if command=="next_frame":
		# media.set_fullscreen(True)
		media.next_frame()
		pass
	else:
    	print("I received command \"%s\" but I don't know what to do with it, yet." % command)


def main(RECEIVE_PORT):
	#OSC server
	# media = inst.media_player_new(FILE)
	print("How many video outputs does this media player have?")
	print(media.has_vout())
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