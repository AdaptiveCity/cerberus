# import the necessary packages
import time
import cv2
import numpy
import json

class DiffBoxes:

    def __init__(self, settings):
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
        self.DIFF_COUNT_THRESHOLD = 0.32
        self.DIFF_COUNT_PIXEL_DELTA = 0.1

        self.threshold = settings["threshold"]

        ## Here we need to select the 'empty' image for left/right/middle camera
        self.image_empty = cv2.imread(empty_image_filename)


    def img_brightness(img):
        cols, rows = img.shape
        brightness_input = numpy.sum(img) / (255 * cols * rows)
        return brightness_input

    def run(self, img):

        start_time = time.time()

        # Calculate the per-element absolute difference between
        # two arrays or between an array and a scalar
        image_diff = img.copy()

        image_diff = cv2.absdiff(image_diff, self.image_empty)

        image_diff = cv2.cvtColor(image_diff, cv2.COLOR_BGR2GRAY)

        for box in self.boxes_obj["seats"]:
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
                if pixels_delta < self.DIFF_COUNT_THRESHOLD:
                    confidence = pixels_delta / self.DIFF_COUNT_THRESHOLD * self.threshold
                else:
                    confidence = self.threshold + (1-self.threshold) * (pixels_delta - self.DIFF_COUNT_THRESHOLD) / (1 - self.DIFF_COUNT_THRESHOLD)
                #confidence = pixels_delta
            else:
                confidence = img_brightness(image_box)

            if confidence > self.threshold:
                self.results["faces"].append({"confidence": confidence, "seat_id": seat_id, "x": x, "y": y, "w": w, "h": h})

        end_time = time.time()

        self.results["metadata"]["inference_time"] = round(end_time - start_time,2)
        self.results["metadata"]["acp_ts"]=str(time.time())
        self.results["metadata"]["img_res"]=str(img.shape)

        return self.results
