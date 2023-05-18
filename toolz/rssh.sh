#!/bin/bash

/home/lt1/cerberus/toolz/waitnet.sh

echo $(date) rssh.sh $1 trying ssh reverse tunnel

ssh -o ExitOnForwardFailure=yes -f -N -T -R $1:localhost:22 jb2328@tfc-app9.cl.cam.ac.uk


# 8022: ijl20-dell7040
# 8023: ijl20-iot
# 8025: adacity-i1
