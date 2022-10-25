#!/usr/bin/env bash
set -eou pipefail

cd /home/pi
git clone https://github.com/KaneBetter/omxplayer.git
cd omxplayer

sudo apt-get update && sudo apt install -y git libasound2-dev libva2 libpcre3-dev libidn11-dev libboost-dev libdbus-1-dev libssh-dev libsmbclient-dev libssl-dev

# see https://github.com/popcornmix/omxplayer/issues/731
sed -i -e 's/git-core/git/g' prepare-native-raspbian.sh
sed -i -e 's/libva1/libva2/g' prepare-native-raspbian.sh
sed -i -e 's/libssl1.0-dev/libssl-dev/g' prepare-native-raspbian.sh
sed -i -e 's/--enable-libsmbclient/--disable-libsmbclient/g' Makefile.ffmpeg

./prepare-native-raspbian.sh
make ffmpeg

make -j$(nproc)
make dist
sudo make install