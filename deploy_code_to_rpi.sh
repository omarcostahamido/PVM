#!/bin/bash

# Get all host ip and save it in to a file
cat max-init.txt | awk '{split($0,a," "); print a[3]}' >> host_ip.txt 2>&1

# Note: run `brew install pdsh` before you run the command below
# ssh into multiple host
# setup passwordless rpi first
# please follow: https://danidudas.medium.com/how-to-connect-to-raspberry-pi-via-ssh-without-password-using-ssh-keys-3abd782688a
pdsh -R ssh -w ^host_ip.txt -l pi
