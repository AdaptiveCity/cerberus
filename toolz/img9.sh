#!/bin/bash

ofile=${1:-test.jpg}
libcamera-still -o $ofile -n --width 4056 --height 3040 --shutter 100000 --gain 1.0

sftp tfc-app9.cl.cam.ac.uk <<EOF
put $ofile
exit
EOF

