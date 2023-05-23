#!/bin/bash

/home/lt1/cerberus/toolz/waitnet.sh

echo $(date) rssh.sh $1 trying ssh reverse tunnel

ssh -o ExitOnForwardFailure=yes -f -N -T -R $1:localhost:22 lt1@tfc-app9.cl.cam.ac.uk

