# import the necessary packages
import time
import cv2
import numpy
import json

class DiffBoxes:

    def __init__(self, settings):

        self.debug_mode = False # this can be toggled True e.g. by putting "seat_id" in settings

        # load the diffboxes metadata
        boxes_filename = "diff_boxes/boxes/boxes_middle.json"
        empty_image_filename = "diff_boxes/images/lt1_middle_empty_1.jpg"
        if settings["position"] == "L":
            boxes_filename = "diff_boxes/boxes/boxes_left.json"
            empty_image_filename = "diff_boxes/images/lt1_left_empty_1.jpg"
        if settings["position"] == "R":
            boxes_filename = "diff_boxes/boxes/boxes_right.json"
            empty_image_filename = "diff_boxes/images/lt1_right_empty_1.jpg"
        json_file = open(boxes_filename)
        self.boxes_obj = json.load(json_file)
        json_file.close()
        print("[INFO] loaded boxes json from {}".format(boxes_filename))

        self.results={"metadata":{"model":"diffboxes"}, "faces":[]}

        self.METHOD = "diff_count"
        self.DIFF_COUNT_THRESHOLD = 0.12  # proportion of pixels that must be different to hit self.threshold
        self.DIFF_COUNT_PIXEL_DELTA = 0.2 # grayscale delta 0..1  for diff_count method to count each pixel

        self.threshold = settings["threshold"]

        try:
            self.seat_id = settings["seat_id"]
            self.debug_mode = True
            print(f'DiffBoxes using seat_id {self.seat_id}')
        except KeyError:
            self.seat_id = None

        ## Here we need to select the 'empty' image for left/right/middle camera
        self.image_empty = cv2.imread(empty_image_filename)


    def img_brightness(img):
        cols, rows = img.shape
        brightness_input = numpy.sum(img) / (255 * cols * rows)
        return brightness_input

    def detect_box(self,image_diff,box):
        x = box["x"]
        y = box["y"]
        w = box["width"]
        h = box["height"]
        x1 = x + w
        y1 = y + h
        seat_id = box["seat_id"]

        #print("seat {} found".format(seat["seat_id"]))

        # make crop of seat box
        image_box = image_diff[y:y1, x:x1]

        # calculate occupied 0..1
        if self.METHOD == "diff_count":
            # What proportion of pixels differ by more than X
            pixels_delta = (image_box > self.DIFF_COUNT_PIXEL_DELTA*255).sum() / (box["width"] * box["height"]) # 0..1

            if self.debug_mode:
                print(f'seat {box["seat_id"]} pixels_delta={pixels_delta}')

            if pixels_delta < self.DIFF_COUNT_THRESHOLD:
                confidence = pixels_delta / self.DIFF_COUNT_THRESHOLD * self.threshold
            else:
                confidence = self.threshold + (1-self.threshold) * (pixels_delta - self.DIFF_COUNT_THRESHOLD) / (1 - self.DIFF_COUNT_THRESHOLD)
            #confidence = pixels_delta
        else:
            confidence = img_brightness(image_box)

        return {"confidence": confidence, "seat_id": seat_id, "x": x, "y": y, "w": w, "h": h}


    def run(self, img):

        start_time = time.time()

        # Calculate the per-element absolute difference between
        # two arrays or between an array and a scalar
        image_diff = img.copy()

        image_diff = cv2.absdiff(image_diff, self.image_empty)

        image_diff = cv2.cvtColor(image_diff, cv2.COLOR_BGR2GRAY)

        if self.seat_id is None:
            for box in self.boxes_obj["seats"]:

                result = self.detect_box(image_diff, box)

                #DEBUG
                if self.debug_mode or result["confidence"] >= self.threshold:
                    self.results["faces"].append(result)
        else:
            print(f'DiffBoxes limiting detect to seat {self.seat_id}')
            for box in self.boxes_obj["seats"]:
                if box["seat_id"] == self.seat_id:
                    result = self.detect_box(image_diff, box)
                    self.results["faces"].append(result)

        end_time = time.time()

        self.results["metadata"]["inference_time"] = round(end_time - start_time,2)
        self.results["metadata"]["acp_ts"]=str(time.time())
        self.results["metadata"]["img_res"]=str(img.shape)

        return self.results
