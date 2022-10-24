# PVM
Pi Video Machine - a scalable, synchronized, and networked-controlled, raspberry pi based, video player machine for video installations


### { This is a work in progress }

## Requirements

- [Python3](https://www.python.org/downloads/)
- [Max/MSP](https://cycling74.com/)

## Installation
### Prerequisites
### Raspberry Pi OS
The recommended Raspberry Pi OS version is:

<img width="569" alt="image" src="https://user-images.githubusercontent.com/51472016/197014809-c39fc6c9-0a08-4b05-92cf-f79fead3c000.png">

To install this to your Raspberry Pi, you need the following things:
+ SD card reader.
+ A laptop (windows/MacOSLinux).

***Steps to install Raspberry OS***:
 + remove the SD card on your Raspberry Pi and read it on your laptop using the SD card reader.
 + Install Raspberry Pi Imager.
    + Mac: https://downloads.raspberrypi.org/imager/imager_latest.dmg
    + Windows: https://downloads.raspberrypi.org/imager/imager_latest.exe
    + Linux: https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb
 + Open the Raspberry Pi Imager:
  + Choose OS:
    
    <img width="680" alt="image" src="https://user-images.githubusercontent.com/51472016/197016636-3106d1e2-8327-4406-816c-fa07f0601f12.png">
    
    + Select Raspberry Pi OS (other):
    
    <img width="680" alt="image" src="https://user-images.githubusercontent.com/51472016/197016751-c49fe6cc-693f-4110-bec1-11ec06441bde.png">
    
    + Scroll down and select the recommended version.
  + Choose Storage.
     + Choose your inserted SD card.
     + Write.
  + After the writing process is finished, insert the SD card with the new OS version into your Raspberry Pi and turn it on.
  + Done.


### Set up environment
Clone or download this repo

Navigate with the terminal to where it is

Create a virtual environment

`python3 -m venv PVM`

Open your venv

`source PVM/bin/activate`

(optional) update pip and setuptools

`pip install --upgrade pip setuptools`

install dependencies

`pip install -r requirements.txt`

(optional) download a sample video

`curl "https://test-videos.co.uk/vids/jellyfish/mp4/h264/720/Jellyfish_720_10s_5MB.mp4" --output jellyfish720p.mp4`


## Running

On each Pi device, start the script

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

On the control machine first edit the `max-init.txt` file. For each Pi device add a numbered line with the video filename, ip, and port. As in:

```
1, jellyfish720.mp4 192.168.1.108 8001;
```

Then proceed to launch the main control patch: `pvm.maxpat`. The `pvm_init` patcher should automatically open and parse the `max-init.txt` file, and configure the multiple `pvm_send` patchers. If some changes were made or reloading is required, simply click the `reset` message box to retrigger this. At this point, the `pvm_control` bpatcher, on the top left portion, should be able to control all devices at the same time. The available controls should be mostly self explanatory: i) the toggle at top left works like a start/stop button; ii) the `next_frame` message box triggers the next frame of the video when it is paused; iii) the `fullscreen` message box toggles the fullscreen display; and iv) the two number boxes below change (and trigger) the `set_position` and `set_rate` commands. Should you want to control just one of the devices or a sub-selection, feel free to delete patch chords accordingly. To operate the warmup system at the bottom right, consisting of the `pvm_warmup` bpatcher, first dial some value in all the four number boxes and then press the toggle to activate it. The (proof of concept) resync system, on the top right portion of the patch, includes a toggle that enables a metro object to force the devices to go to position 0. (i.e. start of the clip) every `n` seconds, where `n` is determined by the number box just above.


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
_           | `pvm_alt.py`                | (to be removed) alternative main python script, this runs on each pi device. Does not use `python-vlc`, instead controls vlc from a terminal stdin
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

## Examples

Navigate to the `examples` folder and open the `examples.maxproj` file.

A series of quick examples appears listed on the Max project window.

Patch `#00.maxpat` serves as an index of the examples provided.

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
