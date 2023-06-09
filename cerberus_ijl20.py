#!/usr/bin/python3
"""
This code is Picamera2 based and thus will only work with Pi camera legacy support mode disabled.
"""
import cv2
import argparse
import time
import json
from classes.jb2328_yunet import Yunet
from classes.jb2328_haar_ijl20 import HaarCascade
from classes.diff_boxes import DiffBoxes
from settings import settings


def capture(img,res):
    #check that we're not duplicating a passed image
    #if it's not a string then a photo, save with custom name
    if not type(img) is str:
        timestamp = time.time()
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))

        filename="cerberus_alpha_"+formatted_time+"_"+str(int(timestamp))
        # Save the current frame as an image
        image_name = "./img/"+filename+".jpg"
        # Using cv2.imwrite() method
        # Saving the image
        cv2.imwrite(image_name,cv2.cvtColor(img, cv2.COLOR_RGB2BGR) )
    #else it's probably not a photo but a string name of an existing photo
    else:
        #save the json file with with an existing filename but different extension
        image_name = img

    #save fd results
    outfile = image_name[:-4]+".json"
    with open(outfile, 'w') as f:
        json.dump(res, f)
        print(f'Wrote JSON to {outfile}')

            # cur.save(image_name)
    print("img captured")

def load_locally(model_name, image_path):
      # Instantiate face detection object here
    score_threshold = None  # Set the threshold if needed

    #temporary if/else for debug purposes:
    if model_name == "Yunet":
        fd_model = Yunet(score_threshold)
    elif model_name == "haarcascade":
        fd_model = HaarCascade()
    elif model_name == "diffboxes":
        fd_model = DiffBoxes()
    else:
        raise ValueError("Invalid model name")

    #load the image
    im = cv2.imread(image_path)

    # Perform face detection here
    results = fd_model.run(im)

    faces=results["faces"]

    print(results["metadata"]["model"]+" detected faces:", len(faces),
            " Inference duration:", results["metadata"]["inference_time"], " seconds")

    if(len(faces)>0):
        print("RESULTS",results)
        capture(image_path, results)

    add_boxes(im, results)
    cv2.imshow("Result", cv2.resize(im, None,fx=0.5,fy=0.5, interpolation = cv2.INTER_AREA))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return

# update img with boxes / labels
def add_boxes(img, results):
    for box in results["faces"]:
        x = box["x"]
        y = box["y"]
        x1 = x + box["w"]
        y1 = y + box["h"]
        color = (100,100,255)
        thickness = 4
        try:
            seat_id = box["seat_id"]
        except KeyError:
            seat_id = ''

        try:
            conf = box["confidence"]
            confidence = f'{conf:.2f}'
        except (KeyError, TypeError):
            confidence = ''

        # Add box to img
        img = cv2.rectangle(img,(x,y),(x1,y1),color, thickness)
        if seat_id != '' or confidence != '':
            img = cv2.putText(img, f'{confidence} {seat_id}',(x+5,y-15), cv2.FONT_HERSHEY_PLAIN, 2, color, 2, cv2.LINE_AA)


def main(model_name, resolution):
    from picamera2 import Picamera2

    last_save = 0
    save_interval=60 #time in seconds

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

    #temporary if/else for debug purposes:
    if model_name == "Yunet":
        fd_model = Yunet(score_threshold)
    elif model_name == "haarcascade":
        fd_model = HaarCascade()
    else:
        raise ValueError("Invalid model name")

    while True:

        im = picam2.capture_array()

        # Perform face detection here
        results = fd_model.run(im)

        faces=results["faces"]

        print(results["metadata"]["model"]+" detected faces:", len(faces),
              " Inference duration:", results["metadata"]["inference_time"], " seconds")

        if(len(faces)>0):
            print("RESULTS",results)
            current_time = time.time()
            print("SAVING IN:",save_interval- int(current_time - last_save) )
            if current_time - last_save > save_interval:
                capture(im, results)
                last_save = current_time


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face detection script using Picamera2.")
    parser.add_argument("-m", "--model", type=str, default="haarcascade",
                        help="Select the face detection model. Default is 'haarcascade'.")
    parser.add_argument("-r", "--resolution", nargs=2, type=int, default=None,
                        help="Set the camera resolution. Pass width and height as two integers, e.g., '-r 1280 720'. Default is config_HQ.")
    parser.add_argument("-i","--image", type=str, default=None,
                        help="Path to the image to be processed. If this argument is provided, the script will process the provided image instead of capturing a new frame.")

    args = parser.parse_args()
    print("settings:",settings)
    if(args.image is None):
        main(args.model, args.resolution)
    else:
        print("loading locally")
        load_locally(args.model, args.image)
