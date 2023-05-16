import cv2

class FaceDetector:
    def __init__(self, model_name, score_threshold=None):
        self.model_name = model_name
        self.score_threshold = score_threshold

        if model_name == "Yunet":
            from backends.yn_backend import YNBackend
            self.model = YNBackend(score_threshold=score_threshold)
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
        else:
            raise ValueError("Invalid model name")

    def run(self, img):
        if self.model_name in ["Yunet", "retinaface", "img2pose", "yoloface"]:
            result=self.model.run(img)
            return [] if result==None else result
        
        elif self.model_name == "haarcascade":
            #haar likes black and white images
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            result=self.model.detectMultiScale(grey, 1.1, 5)
            return result
        
        else:
            raise ValueError("Invalid model name")
