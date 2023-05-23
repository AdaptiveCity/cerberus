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
# from classes.face_detector import FaceDetector

def capture(img,res):
   
    timestamp = time.time()
    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))

    filename="cerberus_alpha_"+formatted_time+"_"+str(int(timestamp))
    # Save the current frame as an image
    image_name = "./img/"+filename+".jpg"
                # Using cv2.imwrite() method
                # Saving the image
    cv2.imwrite(image_name,cv2.cvtColor(img, cv2.COLOR_RGB2BGR) )
    outfile = image_name[:-4]+".json"
    print(res)
    with open(outfile, 'w') as f:
        json.dump(res, f)
        print(f'Wrote JSON to {outfile}')

            # cur.save(image_name)
    print("img captured")

        

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
        start = time.time()
        results = fd_model.run(im)
        end = time.time()
        duration = round(end - start,2)
        
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
                
        results=None
        im=None
           

            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face detection script using Picamera2.")
    parser.add_argument("-m", "--model", type=str, default="haarcascade",
                        help="Select the face detection model. Default is 'haarcascade'.")
    parser.add_argument("-r", "--resolution", nargs=2, type=int, default=None,
                        help="Set the camera resolution. Pass width and height as two integers, e.g., '-r 1280 720'. Default is config_HQ.")

    args = parser.parse_args()
    main(args.model, args.resolution)
