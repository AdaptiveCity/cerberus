#!/usr/bin/python3
"""
This code is Picamera2 based and thus will only work with Pi camera legacy support mode disabled.
"""
import cv2
import argparse
import time
from picamera2 import Picamera2
from face_detector import FaceDetector

def main(model_name, resolution):
    picam2 = Picamera2()

    if resolution:
        width, height = resolution
        config = picam2.create_still_configuration(main={"size": (width, height)})
    else:
        config = picam2.create_still_configuration()

    picam2.configure(config)
    picam2.start()

    # Instantiate face detection object here
    score_threshold = None  # Set the threshold if needed
    fd_model = FaceDetector(model_name, score_threshold)

    while True:
        im = picam2.capture_array()
        # Perform face detection here
        start = time.time()
        results = fd_model.run(im)
        end = time.time()

        duration = round(end - start,2)
        print("Model detected faces:", len(results), " Inference duration:", duration, "seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face detection script using Picamera2.")
    parser.add_argument("-m", "--model", type=str, default="haarcascade",
                        help="Select the face detection model. Default is 'haarcascade'.")
    parser.add_argument("-r", "--resolution", nargs=2, type=int, default=None,
                        help="Set the camera resolution. Pass width and height as two integers, e.g., '-r 1280 720'. Default is config_HQ.")

    args = parser.parse_args()
    main(args.model, args.resolution)
