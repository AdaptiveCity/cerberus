# Face Detection with Picamera2

This Python script uses the Picamera2 library and a face detection wrapper class to perform face detection on images captured from the Raspberry Pi camera. The script allows you to choose the face detection model and the camera resolution through optional command-line arguments.

## Requirements

- Raspberry Pi with Camera Module
- Picamera2 library installed (`pip install picamera2`)
- OpenCV installed (`pip install opencv-python`)
- Face detection models and their corresponding Python libraries

## Usage

1. Make sure the `face_detector.py` file containing the `FaceDetector` wrapper class is in the same directory as the main script.

2. Run the script with optional arguments to select the model and resolution:

`python3 script.py -m <model_name> -r <width> <height>`

### Optional arguments
`-m, --model`: Select the face detection model (default is 'haarcascade'). 

Replace `<model_name>` with the desired model name (e.g., 'Yunet', 'retinaface', 'img2pose', 'yoloface', or 'haarcascade').

`-r, --resolution`: Set the camera resolution by passing `<width>` and `<height>` as two integers (e.g., -r 1280 720). If not provided, the default resolution will be used (config_HQ).

### Examples
To run the script with the default model (haarcascade) and resolution (config_HQ):

`python3 app.py`  

- To run the script with a specific model and resolution:

`python3 script.py -m haarcascade -r 1280 720`   


The script will print the number of detected faces and the inference duration (in seconds) for each captured frame.
