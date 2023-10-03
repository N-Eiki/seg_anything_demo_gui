#!/bin/sh

export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

sudo service x11-common start
sudo service dbus start
gnome-shell --x11 -r