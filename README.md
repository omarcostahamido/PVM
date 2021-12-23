# PVM
Pi Video Machine - a scalable, synchronized, and networked-controlled, raspberry pi video player machine for installation work


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

`python {name-of-script}.py`


## Todo

- explain how to remote control
- add start position offset
- set script autostart