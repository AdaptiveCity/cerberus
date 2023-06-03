import cv2
import time

class HaarCascade:
    def __init__(self, settings):
        self.model = cv2.CascadeClassifier("./backends/haarcascade_frontalface_default.xml")
        self.results={"metadata":{"model":"haarcascade"}, "faces":[]}

    def run(self, img):
        #cleanup
        self.results["metadata"]["acp_ts"]=None
        self.results["metadata"]["img_res"]=None
        self.results["metadata"]["inference_time"] = None
        self.results["faces"]=[]

        #convert to BW, haar likes it
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #run inference and time it
        start_time = time.time()

        # For each resulting detection, levelWeights will then contain the certainty of classification
        # cv.CascadeClassifier.detectMultiScale3(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize[, outputRejectLevels]]]]]]	) ->	objects, rejectLevels, levelWeights
        # image	        Matrix of the type CV_8U containing an image where objects are detected.
        # objects	    Vector of rectangles where each rectangle contains the detected object, the rectangles may be partially outside the original image.
        # numDetections	Vector of detection numbers for the corresponding objects. An object's number of detections is the number of neighboring positively classified rectangles that were joined together to form the object.
        # scaleFactor	Parameter specifying how much the image size is reduced at each image scale.
        # minNeighbors	Parameter specifying how many neighbors each candidate rectangle should have to retain it.
        # flags	        Parameter with the same meaning for an old cascade as in the function cvHaarDetectObjects. It is not used for a new cascade.
        # minSize	    Minimum possible object size. Objects smaller than that are ignored.
        # maxSize	    Maximum possible object size. Objects larger than that are ignored. If maxSize == minSize model is evaluated on single scale.
        faces, _, weights = self.model.detectMultiScale3(grey, scaleFactor=1.1, minNeighbors=5, minSize=(40,40), maxSize=(110,110), outputRejectLevels = True)
        # print()
        # print("FACES:")
        # print(faces)
        # print("LEVELWEIGHTS")
        # print(weights)
        # print()
        # faces=self.model.detectMultiScale(grey, 1.1, 5)
        end_time = time.time()


        if faces is None or len(faces)==0:
            return  self.results

        self.results["metadata"]["inference_time"] = round(end_time - start_time,2)
        self.results["metadata"]["acp_ts"]=str(time.time())
        self.results["metadata"]["img_res"]=str(img.shape)

        i = 0
        for f in faces:
            self.results["faces"].append({
                    'confidence': weights[i]/100,
                    'x': int(f[0]),
                    'y': int(f[1]),
                    'w': int(f[2]),
                    'h': int(f[3])
                    })
            i += 1
        return self.results

