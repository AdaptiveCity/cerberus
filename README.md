# cerberus
A privacy preserving crowd counting system comprised of multiple cameras.

# Setup instructions:  

This is a guide  on how to set up a privacy preseving camera.

## Install Pi OS (Bullseye) and set up the core settings
- Setup hostname as `rp1-ltX`
- Put in `UniOfCam-IoT` details
- Setup UK locale

Once the Pi is on, run:  
`sudo apt update && sudo apt upgrade -y`  

### Enable interfaces:
Run: `sudo raspi-config` 
#### SSH
*Interface -> Enable SSH*
#### VNC (optional)
Then *Interface -> Enable VNC*
#### Camera
Make sure `legacy Pi camera support` is `off`.

### Install Virtualenv Package
Run:   
`python -m pip install pip --upgrade`   
`sudo pip install virtualenv`  

### Install Micro
Run:  
`curl https://getmic.ro | bash`  
`sudo mv micro /usr/bin`  

### Install cv2 dependencies
`sudo apt-get install libatlas-base-dev`  

### Install Coral Accelerator Libraries
With the Accelerator unplugged:
```
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install libedgetpu1-std
```
Then plug in the Coral Accelerator:
`sudo apt-get install python3-pycoral`

### Add `lt1` user 

`sudo adduser lt1`  
Add user to the `video` group so we can access the camera:  
As root:  
`sudo usermod -a -G video lt1`  

Later change write access using `chown` or `chmod` if necessary.  

### Add and `acp` directory

In `/media` as root do `sudo mkdir acp`  
Then `sudo chown -R lt1 ./acp/`  

### Set up Flask Repo
Sets up a temporary backdoor access for debugging.

Change the user to `lt1`:  
`su lt1`  

Clone the repo:  
`git clone https://github.com/jb2328/pi-stillframe.git`  

Open the directory:    
`cd pi-stillframe`  

Create a `venv` and enable Picamera2 library from within the venv:    
`virtualenv venv --system-site-packages`  

Start the `venv`:  
`source venv/bin/activate`  

Run:   
`python app.py`

## Set up Reverse SSH to *tfc-app9*
The following instructions to allow SSH access to **lt1-rpiX**, via *tfc-app9* port XXXX.

#### Reverse SSH Guide


Get the Pi's (**lt1-rpiX**) IP address:
`hostname -I`  

SSH from your local machine as `sudo` (e.g. <span style="color:blue">ab1234</span>) to the Pi.

On **lt1-rpiX**:

as `root`:  
```
ssh-keygen -t rsa
```

Hit `enter`

Run: 
`cat ~/.ssh/id_rsa.pub`

*Copy key to clipboard*

SSH to *tfc-app9* as sudo  

On *tfc-app9*:

`cat >>~/.ssh/authorized_keys`

*Paste that id_rsa.pub copied key*

Hit `enter`, to add a blank line to authorized_keys
Hit `ctrl-D` to end the cat

`Ctrl-D` to close the SSH to *tfc-app9*.

Try the SSH to *tfc-app9* again from **lt1-rpiX**, this time you should connect with no password. `Ctrl-D` to quit SSH and return to **lt1-rpiX** console.

In **lt1-rpiX** console:

`sftp jb2328@tfc-app9.cl.cam.ac.uk`  
`get -r /home/ijl20/ijl20_toolz`  
`exit`  

Enter command:

`micro ijl20_toolz/rssh.sh`  
and replace *ijl20* with <span style="color:blue">ab1234</span>  

Then run (XXXX is a port number):  
`ijl20_toolz/rssh.sh XXXX`  

That should open a reverse SSH tunnel to *tfc-app9* and you should be able to log on to **lt1-rpiX** from *tfc-app9* with the command:

 `ssh (user@)localhost -p XXXX`. From here on you can SSH as `lt1`.  

Move the `ijl20_toolz` directory to `lt1` home dir:

`mv ijl20_toolz ../lt1/`  

Assuming that works, you should add the tunnel command to your **lt1-rpiX** `crontab -e`:

`55 * * * * /home/lt1/ijl20_toolz/rssh.sh XXXX`

That should finalise your reverse ssh setup. 

## Download this repo:

Runs core privacy preserving face detection software.  

Clone the repo:  
`git clone https://github.com/AdaptiveCity/cerberus.git`  

Open the directory:    
`cd cerberus`  

Create a `venv` and enable Picamera2 library from within the venv:    
`virtualenv venv --system-site-packages`  

Start the `venv`:  
`source venv/bin/activate`  
`pip install opencv-python==4.6.0.66`  
`pip install numpy --upgrade`  

Run:   
`python app.py`

## Camera Tests
Several other useful commands to now:

To test out the Picamera2 library:
`libcamera-still -o test.jpg`

Following shutter (param = 1/10 sec) & aperture (manual) works ok in a reasonably lit room, aperture set to about midway:  

`libcamera-hello -t 0 --framerate 1 --width 4056 --height 3040 --preview 100,100,4056,3040 --shutter 100000 --gain 1.0 --info-text "Focus: %focus, Shutter: %exp (us)"`

Some subset of the same params (no framerate, could have much smaller preview) can be used with:  
`libcamera-still --timelapse 1000 --output test.jpg`
Which will continuously update a file 'test.jpg' with a 1000 millisecond, which could be served with Flask.  

## Other additional commands:  
### Change the device's hostname:
In CLI:  
`hostnamectl` - shows the hostname of the server  
`hostnamectl set-hostname 'NEW_HOSTNAME'` - sets the server name to NEW_HOSTNAME  
`hostnamectl` - verify that the hostname has changed  

### Change the Wifi Password  
The wireless configuration on the Raspberry Pi is located in /etc/wpa_supplicant. 

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf` - update the WPA changes  
`sudo reboot` - reboots the device, should boot with WiFi connected







