# Cerberus Toolz

## `img9.sh`

Takes a full resolution image on the pi and sftp's it to lt1@tfc-app9.

## `rssh.sh`

Creates a ssh reverse tunnel to tfc-app9.

Port number etc in `secrets`.

This script is run on reboot and periodically from crontab.

## `settime.sh`

Sets the system date/time by collecting time from a web server.

## `show_img.sh`

Runs the flask app to display current image from camera. Accessible only on UCam-IoT network

## `status.sh`

Displays status of running (or not) cerberus app on this pi.

## `stop.sh`

Stops the running cerberus app on this pi.

## `waitnet.sh`

Loops until detects a successful network connection, then returns.

Can be used to delay other scripts until the network is up.
