#!/bin/bash

# Get all host ip and save it in to a file
cat max-init.txt | awk '{split($0,a," "); print a[3]}' &>> host_ip.txt

# Note: run `brew install pdsh` before you run the command below
# ssh into multiple host
pdsh -R ssh -w host_ip.txt

cd /home/pi

# kill all python process
pkill -9 -f pvm_omx.py

# clean the repo
rm -rf PVM

# TODO: We need to move video into another folder
git clone https://github.com/omarcostahamido/PVM.git

cd PVM
python pvm_omx.py
