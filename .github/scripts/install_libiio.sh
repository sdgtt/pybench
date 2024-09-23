#!/bin/bash

# Set LIBIIO_BRANCH if not set
if [ -z "$LIBIIO_BRANCH" ]; then
    LIBIIO_BRANCH="v0.25"
fi

sudo apt-get -qq update
sudo apt-get install -y git cmake graphviz libavahi-common-dev libavahi-client-dev libaio-dev libusb-1.0-0-dev libxml2-dev rpm tar bzip2 gzip flex bison git libzstd-dev
git clone -b $LIBIIO_BRANCH --single-branch --depth 1 https://github.com/analogdevicesinc/libiio.git
cd libiio
cmake . -DHAVE_DNS_SD=OFF
make
sudo make install
cd ..
rm -rf libiio
