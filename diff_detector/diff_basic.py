# import the necessary packages
import argparse
import imutils
import time
#import dlib
import cv2
import numpy

def img_brightness(img):
    cols, rows = img.shape
    brightness_input = numpy.sum(img) / (255 * cols * rows)
    return brightness_input

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path to occupied input image")

ap.add_argument("-e", "--image_empty", type=str, required=True,
	help="path to empty input image")

ap.add_argument("-b", "--brightness", type=int, required=False, default=0,
	help="brightness value [-127,127]")

args = vars(ap.parse_args())

print("[INFO] loading diff model for {}...".format(args["image"]))

t0 = time.time()

# hsv = True will apply HSV conversion to the images before comparison
hsv = False
blur = False
blur_size = (15,15)

# load the input image from disk, resize it, and convert it from
# BGR to RGB channel ordering (which is what dlib expects)
image_input = cv2.imread(args["image"])

## Calculate input image brightness
brightness_input = img_brightness(cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY))

if blur:
    image_input = cv2.blur(image_input, blur_size)

if hsv:
    image_input = cv2.cvtColor(image_input, cv2.COLOR_BGR2HSV)

print(f'Input image brightness {brightness_input:.2f}')

image_empty = cv2.imread(args["image_empty"])
brightness_empty = img_brightness(cv2.cvtColor(image_empty, cv2.COLOR_BGR2GRAY))
print(f'Empty image brightness {brightness_empty:.2f}')


#cv2.imshow("Empty",image_empty)
image_empty_adj = cv2.convertScaleAbs(image_empty, alpha=1, beta=args["brightness"])

brightness_empty_adj = img_brightness(cv2.cvtColor(image_empty_adj, cv2.COLOR_BGR2GRAY))
print(f'Empty_adj image brightness {brightness_empty_adj:.2f}')

#image_empty_adj = cv2.cvtColor(image_empty, cv2.COLOR_BGR2HSV)
cv2.imshow("Empty adj",image_empty_adj)

if blur:
    image_empty_adj = cv2.blur(image_empty_adj, blur_size)

if hsv:
    image_empty_adj = cv2.cvtColor(image_empty_adj, cv2.COLOR_BGR2HSV)

# Calculate the per-element absolute difference between
# two arrays or between an array and a scalar
image_diff = cv2.absdiff(image_input, image_empty_adj)
#image_diff = cv2.cvtColor(image_diff, cv2.COLOR_HSV2BGR)
image_diff = cv2.cvtColor(image_diff, cv2.COLOR_BGR2GRAY)
brightness_diff = img_brightness(image_diff)
print(f'Diff brightness {brightness_diff:.2f}')

t1 = time.time()
print(f'Execution time: {t1-t0:.3f}')

# show the 'diff' image
cv2.imshow("Diff", image_diff)

cv2.waitKey(0)
cv2.destroyAllWindows()
