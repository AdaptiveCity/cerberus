from mtcnn.mtcnn import MTCNN
import cv2

class MTCNNBackend:

  def __init__(self, score_threshold=0.7):
    self.detector = MTCNN(min_face_size=10, steps_threshold=[0.6,0.7,score_threshold])

  def run(self, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = self.detector.detect_faces(img)
    out = []
    for r in res:
      out.append({'confidence': float(r['confidence']),
                  'x': int(r['box'][0]),
                  'y': int(r['box'][1]),
                  'w': int(r['box'][2]),
                  'h': int(r['box'][3])})
    return out



  
