#!/bin/bash
#
# TRIES TO GET A WEB PAGE UNTIL SUCCESS, I.E. waits for network

WAITURL="http://smartcambridge.org/backdoor/time.png"

LOOPCOUNT=0
LOOPEXIT="f"
SLEEPTIME=20

while ((LOOPCOUNT < 30))  && [[ $LOOPEXIT == "f" ]]; do
    # get the headers from the website, including 'date:'
    CURLRETURN=$(curl --head -s $WAITURL)
    # capture the curl command exit value, 0 means GET OK, 6 or 7 means no network
    CURLEXIT=$?
    # we will exit the loop if curl returns anything other than 6 or 7 for no network
    if (( CURLEXIT != 6 && CURLEXIT != 7 )); then
        LOOPEXIT="t"
    fi
    # echo "curl exit $CURLEXIT so LOOPEXIT is $LOOPEXIT"
    if [[ $LOOPEXIT == "f" ]]; then
        LOOPCOUNT=$((LOOPCOUNT + 1))
        if (( LOOPCOUNT == 10 )) || (( LOOPCOUNT == 20 )); then
            SLEEPTIME=$(( SLEEPTIME * 10 ))
        fi
        echo "$(date) waitnet attempt $LOOPCOUNT. Curl failed to get page, sleeping $SLEEPTIME seconds and retrying..."
        sleep $SLEEPTIME
    fi
done

# Anything other than a zero exit value from curl and we quit here
if (( CURLEXIT != 0 )); then
    echo "$(date) waitnet.sh Failed to get time, aborting"
    exit CURLEXIT
fi

echo $(date) waitnet.sh succeeded

