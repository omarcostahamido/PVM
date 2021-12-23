import vlc
from pythonosc import dispatcher, osc_server, udp_client

# media = vlc.MediaPlayer("jellyfish720p.mp4", "--intf macosx")

#media.set_fullscreen(True)

# media.play()

#media.stop()
def parse_qasm(*args):
    for arg in args:
    	print(arg)


def main(RECEIVE_PORT):
    #OSC server
    callback = dispatcher.Dispatcher()
    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", RECEIVE_PORT), callback)
    callback.map("/PVM", parse_qasm)
    server.serve_forever()

main(8001)