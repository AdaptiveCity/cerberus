import cv2
import time
from backends.yn_backend import YNBackend

class Yunet:
    def __init__(self, score_threshold):
        self.score_threshold = score_threshold
        self.model = YNBackend(score_threshold=self.score_threshold)
        self.results={"metadata":{"model":"Yunet"}, "faces":[]}
    
    def run(self, img):
        #cleanup
        self.results["metadata"]["acp_ts"]=None
        self.results["metadata"]["img_res"]=None
        self.results["metadata"]["inference_time"]=None
        self.results["faces"]=[]
        
        #run inference and time it
        start_time = time.time()
        faces=self.model.run(img)
        end_time = time.time()

            
        if faces is None or len(faces)==0:
            return  self.results

        self.results["metadata"]["inference_time"] = round(end_time - start_time,2)
        self.results["metadata"]["acp_ts"]=str(time.time())
        self.results["metadata"]["img_res"]=str(img.shape)
        
        self.results["faces"]=faces
        return self.results