#!/usr/bin/python3
"""
This code is Picamera2 based and thus will only work with Pi camera legacy support mode disabled.
"""
import cv2
import argparse
import time
import json
from picamera2 import Picamera2
from classes.jb2328_yunet import Yunet
from classes.jb2328_haar import HaarCascade
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
                
    return
            
def main(model_name, resolution):
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
