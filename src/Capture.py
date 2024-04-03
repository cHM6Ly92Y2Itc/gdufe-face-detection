import face_recognition
import cv2
from Database import Database
class Capture:
    def __init__(self) -> None:
        self.video_capture = cv2.VideoCapture(0)
        self.video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.process_this_frame = True
        self.db = Database("face")
    def capture(self):
        while True:
            face_locations = []
            ret, frame = self.video_capture.read()
            assert(ret and "camera error")
            if self.process_this_frame:
                rgb_frame = frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_frame)
                for (top, right, bottom, left) in face_locations:
                    face_image = frame[top:bottom, left:right].copy()
                    result = self.db.get_face(face_image)
                    name = "unknown" 
                    if(result):
                        name=result['name']
                    else:
                        try:
                            self.db.add_face(face_image,f"face{self.db.get_face_count()}")
                        except Exception:
                            pass
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            
    def close(self):
        self.video_capture.release()
    def status(self)->bool:
        return self.process_this_frame
    def stop_detection(self):
        self.process_this_frame=False
    def start_detection(self):
        self.process_this_frame=True
