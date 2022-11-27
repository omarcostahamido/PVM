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

During the first boot, there are some initial configurations necessary, which will be easier to do if you connect the Raspberry Pi device to a physical screen, mouse, and keyboard. Please checkout [this official guide](https://www.raspberrypi.com/documentation/computers/getting-started.html#configuration-on-first-boot) for more details. After that you will be able to connect to it remotely (preferably under the same local network). Please check out "[_How to connect to a Raspberry Pi remotely_](https://github.com/omarcostahamido/PVM/wiki/How-to-connect-to-a-Raspberry-Pi-remotely)" and "[VS Code ssh to Raspberry Pi](https://github.com/omarcostahamido/PVM/wiki/VS-Code-ssh-to-Raspberry-Pi)" in our wiki to learn how to do this!


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

### [Optional]Network Time Protocol(NTP)

NTP is intended to [synchronize](https://en.wikipedia.org/wiki/Synchronize) all participating computers to within a few [milliseconds](https://en.wikipedia.org/wiki/Millisecond). The system time may not be so precisely synchronized between different Raspberry Pi's, which may have an impact on the playback of high frame rate videos.

To use NTP to sync all Raspberry Pis' time in local network, please follow section [Configure NTP Client to be Time Synced with the NTP Server](https://web.archive.org/web/20221112203702/https://rishabhdevyadav.medium.com/how-to-install-ntp-server-and-client-s-on-ubuntu-18-04-lts-f0562e41d0e1).

## Videos

Please save all the videos in the `$HOME/Videos/` folder for autostart. On Rapsberry Pi, your default directory should be `/home/pi/Videos/`.


## Running

On each Pi device, start the script

```bash
cd PVM
# Activate python env
source PVM/bin/activate
# The default port is 8001
python pvm.py
# If you want a different port, example 8002
python pvm.py --port 8002
# Or with launch script
sh launch.sh 8001
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

On the control machine first edit the [max-init.txt](https://github.com/omarcostahamido/PVM/blob/main/max-init.txt) file. For each Pi device add a numbered line with the video filename, ip, and port. 
Please use port 8001 to control the first display, and use any other port for the second display. 
As in:

```
1, jellyfish720.mp4 192.168.1.108 8001;
2, jellyfish720.mp4 192.168.1.108 8002;
```

Then proceed to launch the main control interface: `pvm.maxproj`. The `pvm.maxpat` patch should automatically open. 


## Autostart

on the terminal run

`sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

after the last line add

`@lxterminal -e sh $HOME/PVM/launch.sh 8001`

add one more if you need two videos output

`@lxterminal -e sh $HOME/PVM/launch.sh 8002`

Note: this is assuming that you clone this repo on your raspberry pi in the main /home/pi folder and followed the steps in the <a target="_self" href="#installation">Installation</a> section above.

## Structure

* [examples/](./PVM/examples) #example use cases to test our system
  * [#00.maxpat](./PVM/examples/#00.maxpat)
  * [#01.maxpat](./PVM/examples/#01.maxpat)
  * [#02.maxpat](./PVM/examples/#02.maxpat)
  * [#03.maxpat](./PVM/examples/#03.maxpat)
  * [#04.maxpat](./PVM/examples/#04.maxpat)
  * [#05.maxpat](./PVM/examples/#05.maxpat)
  * [examples.maxproj](./PVM/examples/examples.maxproj) #main example patch, contains 5 examples
* [lib/](./PVM/lib) #lib folder to store all maxpat libs
  * [pvm.maxpat](./PVM/lib/pvm.maxpat) #Max project file. Openning this file will load all main control patches.
  * [pvm_control.maxpat](./PVM/lib/pvm_control.maxpat) #abstraction with the control patch GUI to be embedded as a bpatcher
  * [pvm_init.maxpat](./PVM/lib/pvm_init.maxpat) #abstraction responsible for parsing the `max-init.txt` file
  * [pvm_send.maxpat](./PVM/lib/pvm_send.maxpat) #abstraction for OSC sending. Arguments: _ip port_. Attributes: `@ip` `@port`
  * [pvm_warmup.maxpat](./PVM/lib/pvm_warmup.maxpat) #abstraction for interpolating playback rates, to be embedded as a bpatcher
* [.gitattributes](./PVM/.gitattributes)
* [.gitignore](./PVM/.gitignore)
* [LICENSE](./PVM/LICENSE)
* [README.md](./PVM/README.md)
* [build_omxplayer.sh](./PVM/build_omxplayer.sh) #shell script to build `omxplayer` with one _click_
* [deploy_code_to_rpi.sh](./PVM/deploy_code_to_rpi.sh) #shell script to deploy code to Raspberry Pi
* [launch.sh](./PVM/launch.sh) #shell script to start `pvm.py` with `sh launch.sh <port>`
* [max-init.txt](./PVM/max-init.txt) #this file can make control patch setup faster
* [pvm.maxproj](./PVM/pvm.maxproj) #main control patch. controls 6 pvm devices at the same time
* [pvm.py](./PVM/pvm.py) #main python script, this runs on each pi device
* [requirements.txt](./PVM/requirements.txt) #requirement for system python deps
* [test.py](./PVM/test.py) #test python script to test our UDP connection


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

## Development

### Logs
Logs will be recorded by `pvm.py` during execution. These will be stored in the `log/` folder, within the install directory of `PVM` on the Raspberry Pi device. This folder will be created if it doesn't exist yet.

Name convention for each log file is `{:%Y-%m-%d %H:%M:%S}-$PORT.log`

All output from the console is synchronized to the file in real-time.

```bash
2022-11-20 11:32:55.243;INFO;8001;Logging system initiated
2022-11-20 11:32:55.243;INFO;8001;PVM - Pi Video Machine
2022-11-20 11:32:55.244;INFO;8001;Omar Costa Hamido 2022
2022-11-20 11:32:55.244;INFO;8001;Server now listenning on port 8001
```

If you close the program and then reopen it, a new log file will be created.

## Run the test

You could write tests for your combination of commands in the `test.py` file. Simply run `python3 test.py` on the console to perform the tests. When the test script is started, it will first **kill any existing `pvm.py` processes**, and then spawn a new one to test the commands, and end it again after test is finished.

## Helpful links
- https://python-omxplayer-wrapper.readthedocs.io/en/latest/

Also don't forget to checkout our [wiki](https://github.com/omarcostahamido/PVM/wiki)! It contains instructions on various topics like [_setting up remote access to the Raspberry Pi_](https://github.com/omarcostahamido/PVM/wiki/How-to-connect-to-a-Raspberry-Pi-remotely) ,[_VS Code ssh to Raspberry Pi_](https://github.com/omarcostahamido/PVM/wiki/VS-Code-ssh-to-Raspberry-Pi) and [_The workflow in MAX_](https://github.com/omarcostahamido/PVM/wiki/The-workflow-in-MAX).