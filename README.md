# PVM
Pi Video Machine - a scalable, synchronized, and networked-controlled, raspberry pi based, video player machine for video installations


### { This is a work in progress }

## Requirements

- [Python3](https://www.python.org/downloads/)
- [Max/MSP](https://cycling74.com/)

## Installation

Clone or download this repo

Navigate with the terminal to where it is

Create a virtual environment

`python3 -m venv PVM`

Open your venv

`source PVM/bin/activate`

(optional) update pip and setuptools

`pip install --upgrade pip setuptools`

install dependencies

`pip install python-vlc python-osc`

(optional) download a sample video

`curl "https://test-videos.co.uk/vids/jellyfish/mp4/h264/720/Jellyfish_720_10s_5MB.mp4" --output jellyfish720p.mp4`


## Running

Start the script

`python pvm.py`


## Autostart

on the terminal run

`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

after the last line add

`@lxterminal -e sh /home/pi/PVM/launch.sh`

Note: this is assuming that you clone this repo on your raspberry pi in the main /home/pi folder and followed the steps in the <a target="_self" href="#installation">Installation</a> section above.


## Todo

- add help options
- explain how to remote control
- add start position offset


## Helpful links
- https://www.raspberrypi.com/documentation/computers/remote-access.html#vnc
- https://wiki.videolan.org/VLC_command-line_help/
- https://www.videolan.org/vlc/download-windows.html
  - Already comes pre-installed with rpi4
- https://www.olivieraubert.net/vlc/python-ctypes/doc/
- https://www.geeksforgeeks.org/vlc-module-in-python-an-introduction/
- [forum thread: Rpi4: YouTube Full HD 1080p is slow! How to fix?](https://forums.raspberrypi.com/viewtopic.php?t=302787)


## Known limitations
- as of [v0.2.1](https://github.com/omarcostahamido/PVM/releases) videos only repeat 65535 times (see [here](https://omarcostahamido.com/pvm) helper tool)
  - this is no longer the case with the current experimental version `pvm_alt.py`
