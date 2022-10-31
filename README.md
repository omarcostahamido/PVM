# PVM
Pi Video Machine - a scalable, synchronized, and networked-controlled, raspberry pi based, video player machine for video installations


### { This is a work in progress }

- TODO: Create another python file to control two display


## Requirements

- [Python3](https://www.python.org/downloads/)
- [Max/MSP](https://cycling74.com/)


## Installation

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


### Connect to a Raspberry Pi

During the first boot, there are some initial configurations necessary, which will be easier to do if you connect the Raspberry Pi device to a physical screen, mouse, and keyboard. Please checkout [this official guide](https://www.raspberrypi.com/documentation/computers/getting-started.html#configuration-on-first-boot) for more details. After that you will be able to connect to it remotely (preferably under the same local network). Please check out "[_How to connect to a Raspberry Pi remotely_](https://github.com/omarcostahamido/PVM/wiki/How-to-connect-to-a-Raspberry-Pi-remotely)" our wiki to learn how to do this!


### OMXPlayer

To build the customized OMXPlayer, run the command below:

`./build_omxplayer.sh`


### Set up environment

```bash
# Clone the repo
git clone https://github.com/omarcostahamido/PVM.git

cd PVM

# Create a virtual environment
python3 -m venv PVM

# Activate venv
source PVM/bin/activate

# Update pip and setuptools
pip install --upgrade pip setuptools

# Install dependencies
pip install -r requirements.txt

# (Optional) Download a sample video
curl "https://test-videos.co.uk/vids/jellyfish/mp4/h264/720/Jellyfish_720_10s_5MB.mp4" --output jellyfish720p.mp4
```


## Videos

Please save all the videos in the `/home/pi/Videos/` folder for autostart.


## Running

On each Pi device, start the script

```bash
cd PVM
python pvm.py
```

Read the help

`python pvm.py --help`

```bash
usage: pvm.py [-h] [--port [PORT]]

optional arguments:
  -h, --help     show this help message and exit
  --port [PORT]  The port that pvm.py will use to receive control messages.
                 Default port is 8001
```

On the control machine first edit the [max-init.txt](https://github.com/omarcostahamido/PVM/blob/main/max-init.txt) file. For each Pi device add a numbered line with the video filename, ip, and port. As in:

```
1, jellyfish720.mp4 192.168.1.108 8001;
```

Then proceed to launch the main control interface: `pvm.maxproj`. The `pvm.maxpat` patch should automatically open. 


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
**control** | `max-init.txt`              | this file can make control patch setup faster
_           | `pvm.maxpat`                | main control patch. controls 6 pvm devices at the same time
_           | `pvm_control.maxpat`        | abstraction with the control patch GUI to be embedded as a bpatcher
_           | `pvm_init.maxpat`           | abstraction responsible for parsing the `max-init.txt` file
_           | `pvm_send.maxpat`           | abstraction for OSC sending. Arguments: _ip port_. Attributes: `@ip` `@port` 
_           | `pvm_warmup.maxpat`         | abstraction for interpolating playback rates, to be embedded as a bpatcher
_           | `pvm.maxproj`               | Max project file. Openning this file will load all main control patches.
_           | `host.py`                   | (to be removed) control a remote device using a python script instead
**others**  | `launch.sh`                 | shell script to start `pvm.py` with one _click_
_           | `build_omxplayer.sh`                 | shell script to build `omxplayer` with one _click_


## How to deploy your code when you testing in multiple rpis?
Use the [deploy_code_to_rpi.sh](https://github.com/omarcostahamido/PVM/blob/AddCDscript/deploy_code_to_rpi.sh) script.
But there are two prerequisites:

One is the need to set up passwordless ssh access.
For the passwordless ssh access please follow [here](https://danidudas.medium.com/how-to-connect-to-raspberry-pi-via-ssh-without-password-using-ssh-keys-3abd782688a).

Second is the need to set the [autostart](https://github.com/omarcostahamido/PVM#autostart).

Once you're done, run the command on the control pc.

```bash
bash deploy_code_to_rpi.sh

# Download the latest code on RPIs with the IP address in host_ip.txt.
cd PVM && git pull

sudo reboot
```

## Logs

All logs for each time each RPI is stored in the log folder.

Name convention for each file is `{:%Y-%m-%d %H:%M:%S}.log`

All output from the console is synchronized to the file in real-time.

```bash
2022-10-31 13:34:21;INFO;Received command: file
2022-10-31 13:34:21;INFO;Received value: jellyfish720p.mp4
2022-10-31 13:34:21;INFO;File set: /home/pi/Videos/jellyfish720p.mp4
```

If you close the program and then reopen it, a new log file will be created.

## Examples

Navigate to the `examples` folder and open the `examples.maxproj` file.

A series of quick examples appears listed on the Max project window.

Patch `#00.maxpat` serves as an index of the examples provided.

Given the objective of making this project available to creative artists, the control interface was created as a Max project. The patch `pvm.maxpat` that opens automatically contains several objects and different abstractions that work together to generate/format and send the control messages to the PVM devices. The `pvm_init` patcher should automatically open and parse the `max-init.txt` file, and configure the multiple `pvm_send` patchers. If some changes were made or reloading is required, simply click the `reset` message box to retrigger this. 

At this point, the `pvm_control` bpatcher, on the top left portion, should be able to control all devices at the same time. The available controls should be mostly self explanatory: 

i) the toggle at top left works like a start/stop button; 

ii) the `next_frame` message box triggers the next frame of the video when it is paused; 

iii) the `fullscreen` message box toggles the fullscreen display;

iv) the two number boxes below change (and trigger) the `set_position` and `set_rate` commands. 

Should you want to control just one of the devices or a sub-selection, feel free to delete patch chords accordingly. To operate the warmup system at the bottom right, consisting of the `pvm_warmup` bpatcher, first dial some value in all the four number boxes and then press the toggle to activate it. 

The (proof of concept) resync system, on the top right portion of the patch, includes a toggle that enables a metro object to force the devices to go to position 0. (i.e. start of the clip) every `n` seconds, where `n` is determined by the number box just above.


## Helpful links
- https://www.raspberrypi.com/documentation/computers/remote-access.html#vnc
- [forum thread: Rpi4: YouTube Full HD 1080p is slow! How to fix?](https://forums.raspberrypi.com/viewtopic.php?t=302787)
- https://python-omxplayer-wrapper.readthedocs.io/en/latest/

Also don't forget to checkout our [wiki](https://github.com/omarcostahamido/PVM/wiki)! It contains instructions on various topics like [_setting up remote access to the Raspberry Pi_](https://github.com/omarcostahamido/PVM/wiki/How-to-connect-to-a-Raspberry-Pi-remotely) and how to run the examples.


## Known limitations
