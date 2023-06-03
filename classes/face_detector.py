import cv2
import time

class FaceDetector:
    def __init__(self, model_name, score_threshold=None):
        self.model_name = model_name
        self.score_threshold = score_threshold
        self.results={"metadata":{}, "faces":[]}

        if model_name == "Yunet":
            from backends.yn_backend import YNBackend
            self.model = YNBackend(score_threshold=self.score_threshold)
            self.results["metadata"]["model"]="Yunet"
            
        elif model_name == "retinaface":
            # Import and instantiate the RetinaFace model here
            pass
        elif model_name == "img2pose":
            # Import and instantiate the img2pose model here
            pass
        elif model_name == "yoloface":
            # Import and instantiate the YOLOFace model here
            pass
        elif model_name == "haarcascade":
            self.model = cv2.CascadeClassifier("./backends/haarcascade_frontalface_default.xml")
            self.results["metadata"]["model"]="haarcascade"

        else:
            raise ValueError("Invalid model name")

    def run(self, img):
        #cleanup
        self.results["metadata"]["acp_ts"]=None
        self.results["metadata"]["img_res"]=None
        self.results["faces"]=[]
        
        if self.model_name in ["Yunet", "retinaface", "img2pose", "yoloface"]:
            
            faces=self.model.run(img)
            
            #return [] if result==None else result
            if faces is None or len(faces)==0:
                return  self.results

            self.results["metadata"]["acp_ts"]=str(time.time())
            self.results["metadata"]["img_res"]=str(img.shape)
            
            self.results["faces"]=faces
            
            return self.results
            
        
        elif self.model_name == "haarcascade":
            
            #haar likes black and white images
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces=self.model.detectMultiScale(grey, 1.1, 5)

            if faces is None or len(faces)==0:
                return  self.results  # Return an empty list if no faces are detected
            
            self.results["metadata"]["acp_ts"]=str(time.time())
            self.results["metadata"]["img_res"]=str(img.shape)

            self.results["faces"]=[]
            
            for f in faces:
                self.results["faces"].append({
                        'confidence': None,
                        'x': int(f[0]), 
                        'y': int(f[1]), 
                        'w': int(f[2]), 
                        'h': int(f[3])
                        })
  
            return self.results
        
        else:
            raise ValueError("Invalid model name")
