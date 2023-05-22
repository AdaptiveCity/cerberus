# import the necessary packages
import argparse
import imutils
import time
#import dlib
import cv2
import numpy
import json

def img_brightness(img):
    cols, rows = img.shape
    brightness_input = numpy.sum(img) / (255 * cols * rows)
    return brightness_input

def setup_args():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str, required=True,
    	help="path to occupied input image")

    ap.add_argument("-e", "--image_empty", type=str, required=True,
    	help="path to empty input image")

    ap.add_argument("-b", "--brightness", type=int, required=False, default=0,
    	help="brightness value [-127,127]")

    ap.add_argument("-t", "--threshold", type=float, required=False, default=0.1,
    	help="diff threshold value occupied/empty value [0.1]")

    ap.add_argument("-j", "--json", type=str, required=False, default="boxes/seat_boxes.json",
    	help="Seat boxes json file (seat_boxes.json)")

    ap.add_argument("-m", "--method", type=str, required=False, default="avg_diff",
    	help="Method to calculate diff error avg_diff|diff_count")

    return vars(ap.parse_args())

def main():

    args = setup_args()

    print("[INFO] loading diff_boxes detector for {}...".format(args["image"]))

    json_file = open(args["json"])
    seat_boxes_obj = json.load(json_file)
    json_file.close()

    print("[INFO] loaded seat boxes json from {}".format(args["json"]))

    # load the input image from disk, resize it, and convert it from
    # BGR to RGB channel ordering (which is what dlib expects)

    # read images

    image_input = cv2.imread(args["image"])
    image_empty = cv2.imread(args["image_empty"])

    start_time = time.time()

    #image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2HSV)

    ## Calculate input image brightness
    brightness_input = img_brightness(cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY))

    print(f'[INFO] Input image brightness {brightness_input:.2f}')

    brightness_empty = img_brightness(cv2.cvtColor(image_empty, cv2.COLOR_BGR2GRAY))
    print(f'[INFO] Empty image brightness {brightness_empty:.2f}')

    #cv2.imshow("Empty",image_empty)
    image_empty_adj = cv2.convertScaleAbs(image_empty, alpha=1, beta=args["brightness"])

    brightness_empty_adj = img_brightness(cv2.cvtColor(image_empty_adj, cv2.COLOR_BGR2GRAY))
    print(f'[INFO] Empty_adj image brightness {brightness_empty_adj:.2f}')

    #image_empty_adj = cv2.cvtColor(image_empty, cv2.COLOR_BGR2HSV)

    #cv2.convertScaleAbs(image_empty, contrast 0..1..+ve, brightness [-127, 127])
    #cv2.imshow("Empty", image_empty)

    # Calculate the per-element absolute difference between
    # two arrays or between an array and a scalar
    image_diff = image_input.copy()

    image_diff = cv2.absdiff(image_diff, image_empty_adj)
    #image_diff = cv2.cvtColor(image_diff, cv2.COLOR_HSV2BGR)
    image_diff = cv2.cvtColor(image_diff, cv2.COLOR_BGR2GRAY)

    for seat in seat_boxes_obj["seats"]:
        x = seat["x"]
        y = seat["y"]
        x1 = x + seat["width"]
        y1 = y + seat["height"]
        #print("seat {} found".format(seat["seat_id"]))

        # make crop of seat box
        image_seat = image_diff[y:y1, x:x1]

        # calculate occupied 0..1
        if args["method"] == "diff_count":
            # What proportion of pixels differ by more than X
            occupied = (image_seat > 40).sum() / (seat["width"] * seat["height"])
        else:
            occupied = img_brightness(image_seat)

        if occupied > args["threshold"]:
            color = (100,100,255)
            thickness = 4
        else:
            color = (200,200,200)
            thickness = 1
        image_input = cv2.rectangle(image_input,(x,y),(x1,y1),color, thickness)
        image_input = cv2.putText(image_input, f'{occupied:.2f}',(x+5,y+25), cv2.FONT_HERSHEY_PLAIN, 2, color, 2, cv2.LINE_AA)


    finish_time = time.time()

    #image_input = imutils.resize(image_input, width=2000)
    #rgb_image = cv2.cvtColor(image_input, cv2.COLOR_BGR2RGB)
    # perform face detection using dlib's face detector

    #print("[INFO[ performing face detection with OpenCV...")
    #boxes = detector.detectMultiScale(image_input)
    #end = time.time()
    #print("[INFO] face detection found {} faces and took {:.4f} seconds".format(len(boxes), end - start))

    # loop over the bounding boxes
    #for (x, y, w, h) in boxes:
    #    # draw the bounding box on our image
    #    cv2.rectangle(image_input, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #    print("detected face at ({},{}) size ({},{})".format(x,y,w,h))

    # show the output image
    #cv2.imwrite('haar_result.jpg', image_input)
    cv2.imshow("Empty adj",image_empty_adj)
    cv2.imshow("Diff", image_diff)
    cv2.imshow("Input", cv2.resize(image_input, None,fx=0.5,fy=0.5, interpolation = cv2.INTER_AREA))

    print(f'Execution time: {finish_time - start_time:.3f}')

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
