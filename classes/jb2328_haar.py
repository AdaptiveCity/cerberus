import cv2
import time

class HaarCascade:
    def __init__(self):
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
        faces=self.model.detectMultiScale(grey, 1.1, 5)
        end_time = time.time()


        if faces is None or len(faces)==0:
            return  self.results
        
        self.results["metadata"]["inference_time"] = round(end_time - start_time,2)
        self.results["metadata"]["acp_ts"]=str(time.time())
        self.results["metadata"]["img_res"]=str(img.shape)

        for f in faces:
            self.results["faces"].append({
                    'confidence': None,
                    'x': int(f[0]), 
                    'y': int(f[1]), 
                    'w': int(f[2]), 
                    'h': int(f[3])
                    })

        return self.results

