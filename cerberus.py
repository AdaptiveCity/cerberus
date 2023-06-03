#!/usr/bin/python3
"""
This code is Picamera2 based and thus will only work with Pi camera legacy support mode disabled.
"""
import cv2
import argparse
import time
import json
import importlib

from classes.jb2328_yunet import Yunet
from classes.jb2328_haar import HaarCascade
from classes.diff_boxes import DiffBoxes

from settings.default import settings

# ####################################################################### #
# run_detect - the execution loop used for normal sensor operation        #
# ####################################################################### #

def save_img_and_json(img,res):
    #check that we're not duplicating a passed image
    #if it's not a string then a photo, save with custom name
    if not type(img) is str:        
        #get the timestamp from when the inference was done
        timestamp = float(res["metadata"]["acp_ts"])
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))
        camera_name=settings["acp_id"]
        filename=camera_name+"_"+formatted_time+"_"+str(int(timestamp))
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
    print("img recorded")

def run_detect(fd_model, settings):
    from picamera2 import Picamera2

    last_save = 0
    #set saving frequency, default is 60s
    save_interval = settings["frequency"] #time in seconds
    
    picam2 = Picamera2()

    if settings["resolution"]:
        width, height = settings["resolution"]
        config = picam2.create_still_configuration(main={"size": (width, height)})
    else:
        config = picam2.create_still_configuration()

    picam2.configure(config)
    picam2.start()

    while True:

        im = picam2.capture_array()

        #read settings and rotate image if necessary
        if settings["position"] != "M":
            im = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Perform face detection here
        results = fd_model.run(im)

        faces=results["faces"]

        print(results["metadata"]["model"]+" detected faces:", len(faces),
              " Inference duration:", results["metadata"]["inference_time"], " seconds")

        if(len(faces)>0):
            # print("RESULTS",results)
            current_time = time.time()
            print("SAVING IN:",save_interval- int(current_time - last_save) )
            if current_time - last_save > save_interval:
                save_img_and_json(im, results)
                last_save = current_time

# ####################################################################### #
# detect_local_image - called when run with -i image                      #
# ####################################################################### #
      
def detect_local_image(fd_model, settings, image_path):
    """
    Called if -i parameter is given with an image path.
    Will run the chosen detector on that image, optionally display picture overlaid with detect boxes.
    """

    #load the image
    im = cv2.imread(image_path)
    
    #read settings and rotate image if necessary
    # if settings["position"] != "M":
    #     im = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Perform face detection here
    results = fd_model.run(im)

    faces = results["faces"]

    print(results["metadata"]["model"]+" detected faces:", len(faces),
            " Inference duration:", results["metadata"]["inference_time"], " seconds")

    if(len(faces)>0):
        # print("RESULTS",results)
        save_img_and_json(image_path, results)

    add_boxes(im, results)

    if(args.display):
        cv2.imshow("Result", cv2.resize(im, None,fx=0.5,fy=0.5, interpolation = cv2.INTER_AREA))
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return

# update img with boxes / labels
def add_boxes(img, results):
    """
    Given an image and a results containing the detection boxes,
    overlays the boxes and seat_id's onto the image
    """
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
       
# ####################################################################### #
# main - run from command line                                            #
# ####################################################################### #

def get_model(model_name, settings):
    """
    Given a string name and settings dict, return an instantiated detect model
    """
    fd_model = None
    model_name = model_name.lower()
    if model_name == "yunet":
        fd_model = Yunet(settings)
    elif model_name == "haarcascade":
        fd_model = HaarCascade(settings)
    elif model_name == "diffboxes":
        fd_model = DiffBoxes(settings)
    else:
        raise ValueError("Invalid model name")
    return fd_model

# def adjust_rotation(img, debug=False):
    
#     # print(settings["position"]!="M",settings["position"])
    
#     if(settings["position"]!="M"):
#         if(debug):
#             print("Image is sideways, rotating clockwise...")
#         #Rotate the image 90 degrees clockwise
#         img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
#     else:
#         if(debug):
#             print("Provided image is the right orientation")
        
#     return img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face detection script using Picamera2.")

    parser.add_argument("-s", "--settings", type=str, default="default",
                        help='Filename in settings/ (without.py) for settings. Default "default".')
    parser.add_argument("-m", "--model", type=str, default=settings["model"],
                        help="Select the face detection model. Default is "+str(settings["model"])+".")
    parser.add_argument("-r", "--resolution", nargs=2, type=int, default=None,
                        help="Set the camera resolution. Pass width and height as two integers, e.g., '-r 1280 720'. Default is config_HQ.")
    parser.add_argument("-i","--image", type=str, default=None,
                        help="Path to the image to be processed. If this argument is provided, the script will process the provided image instead of capturing a new frame.")
    parser.add_argument("-f", "--frequency", type=int, default=settings["frequency"],
                        help="Set the capture frequency duration in seconds. Default is "+str(settings["frequency"])+".")
    parser.add_argument("-t", "--threshold", type=float, default=None,
                        help="Set threshold used by detect model. Overrides settings value.")
    parser.add_argument("-d", "--display", action="store_true",
                    help="Show image flag. If set, the image will be displayed.")
    # parser.add_argument("-s", "--save", action="store_true",
    #                     help="Save image flag. If set, the image will be saved.")

    args = parser.parse_args()

    # Load settings
    if args.settings is not None:
        # use -s argument
        settings = importlib.import_module("settings."+args.settings).settings

    print("settings:",settings)
    print("optional args:",args)

    # Add command line args to settings
    if args.threshold is not None:
        settings["threshold"] = args.threshold

    if args.frequency is not None:
        settings["frequency"] = args.frequency

    if args.resolution is not None:
        settings["resolution"] = args.resolution

    # Get the model
    if args.model is not None:
        fd_model = get_model(args.model, settings)
    else:
        fd_model = get_model(settings.model, settings)

    # Either loop on camera, or run for single image
    if args.image is None:
        run_detect(fd_model, settings)
    else:
        print(f'detecting local image {args.image}')
        detect_local_image(fd_model, settings, args.image)
