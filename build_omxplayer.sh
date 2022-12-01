#!/usr/bin/env bash
# How to run this?
# In your console, just run `./build_omxplayer.sh`
set -eou pipefail

cd /home/pi
# Check if omxplayer exists
if [ -d "/omxplayer" ] 
then
	echo "Directory /omxplayer exists, run git pull" 
	cd omxplayer
	git pull
else
	echo "Directory /omxplayer does not exists, clone from github."
	git clone https://github.com/KaneBetter/omxplayer.git
	cd omxplayer
fi

# Update apt and install requirments
sudo apt-get update && sudo apt install -y git libasound2-dev libva2 libpcre3-dev libidn11-dev libboost-dev libdbus-1-dev libssh-dev libsmbclient-dev libssl-dev

# See https://github.com/popcornmix/omxplayer/issues/731
sed -i -e 's/git-core/git/g' prepare-native-raspbian.sh
sed -i -e 's/libva1/libva2/g' prepare-native-raspbian.sh
sed -i -e 's/libssl1.0-dev/libssl-dev/g' prepare-native-raspbian.sh
sed -i -e 's/--enable-libsmbclient/--disable-libsmbclient/g' Makefile.ffmpeg

./prepare-native-raspbian.sh
make ffmpeg

# Copy new version of omxplayer into your system path
make -j$(nproc)
make dist
sudo make install
# Now you can use new version of omxplayer in your console,
# example, omxplayer jellyfish.mp4