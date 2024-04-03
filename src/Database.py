from facedb import FaceDB
import cv2
class Database:
    def __init__(self,dbpath:str) -> None:
        self.db = FaceDB(path=dbpath,module='face_recognition')

    def get_face(self,face):
        return self.db.recognize(img=face,include=['name'])

    def add_face(self,img,name:str)->str:
        return self.db.add(name,img)

    def get_face_count(self)->int:
        return self.db.count()
    
    def get_all_faces_info(self)->list[dict]:
        """
            Get all faces info, include id and name.
        Returns:
            [{"id": str,"name": str}]
        """
        data = self.db.all(include=["id","name"])
        return [{"id":get["id"],"name":get["name"]} for get in data]

    def edit_name(self,name:str,face_id:str)->None:
        self.db.update(id=face_id,name=name)

    def get_face_img(self,face_id:str):
        result = self.db.get(id=face_id,include=['img'])
        ret,img= cv2.imencode('.jpg', result['img'])
        if(ret):
            return img.tobytes()
        return None
    def delete_face(self,id:str):
        self.db.delete(id=id)
        
if __name__=="__main__":
    db = Database("face")
    faces = db.get_all_faces_info()
    print(faces)
    print(db.get_face_count())