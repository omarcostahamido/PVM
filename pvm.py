import vlc
# from pythonosc import dispatcher, osc_server, udp_client
import socket

media = vlc.MediaPlayer("jellyfish720p.mp4")

#media.set_fullscreen(True)

# media.play()

#media.stop()
# def parse_qasm(*args):
#     for arg in args:
#     	print(arg)


# def main(RECEIVE_PORT):
#     #OSC server
#     callback = dispatcher.Dispatcher()
#     server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", RECEIVE_PORT), callback)
#     callback.map("/PVM", parse_qasm)
#     server.serve_forever()

# main(8001)


UDP_IP = ""
UDP_PORT = 8000 #add possibility to change this

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    data = data.decode('UTF-8').split()
    command = data[0]
    argument = data[1]
    if command=="start":
    	media.play()
    	pass
    if command=="stop":
    	media.stop()
    	pass
    if command=="set_position":
		media.set_position(float(data[1]))
    	pass
    if command=="fullscreen":
    	# media.set_fullscreen(True)
    	media.toggle_fullscreen()
    	pass
    else:
    	print("I received command \"%s\" but I don't know what to do with it, yet." % data)