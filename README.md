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

Read the help

`python pvm.py --help`

```
usage: pvm.py [-h] [--port [PORT]]

optional arguments:
  -h, --help     show this help message and exit
  --port [PORT]  The port that pvm.py will use to receive control messages.
                 Default port is 8001
```

## Autostart

on the terminal run

`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

after the last line add

`@lxterminal -e sh /home/pi/PVM/launch.sh`

Note: this is assuming that you clone this repo on your raspberry pi in the main /home/pi folder and followed the steps in the <a target="_self" href="#installation">Installation</a> section above.


## Structure

_           | filename                    | description
---------:  | :-----------                | :---------------------------------------------------
**device**  | `pvm.py`                    | main python script, this runs on each pi device
_           | `pvm_alt.py`                | (to be removed) alternative main python script, this runs on each pi device
**control** | `max-init.txt`              | this file can make control patch setup faster
_           | `pvm.maxpat`                | main control patch. controls 6 pvm devices at the same time
_           | `pvm_control.maxpat`        | abstraction with the control patch GUI to be embedded as a bpatcher
_           | `pvm_init.maxpat`           | abstraction responsible for parsing the `max-init.txt` file
_           | `pvm_send.maxpat`           | abstraction for OSC sending. Arguments: _ip port_. Attributes: `@ip` `@port` 
_           | `pvm_warmup.maxpat`         | abstraction for interpolating playback rates, to be embedded as a bpatcher
_           | `host.py`                   | (to be removed) control a remote device using a python script instead
**others**  | `doc_vlc_-I_rc.txt`         | help log from `vlc` interactive mode CLI
_           | `doc_vlc_-h_--advanced.txt` | help log from `vlc` advanced options CLI
_           | `launch.sh`                 | shell script to start `pvm.py` with one _click_


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
