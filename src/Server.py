from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
from Capture import Capture
from Database import Database

app = Flask(__name__)
CORS(app)
capture = Capture()
db = Database("face")
@app.get('/video_feed')
def video_feed():
    return Response(capture.capture(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/command/detection_control')
def control_detection():
    data=request.get_json()
    if(data["enable"]):
        capture.start_detection()
    else:
        capture.stop_detection()
    return jsonify({"enable":capture.status()})

@app.post('/update')
def update_face():
    data=request.get_json()
    if data['action']=='update':
        if data['name'] and data['id']:
            db.edit_name(data['name'],data['id'])
            return jsonify({"success":True})

    if data['action']=='remove':
        if data['id']:
            db.delete_face(data['id'])
            return jsonify({"success":True})

    return jsonify({"success":False})

@app.get('/detection_status')
def get_detection_status():
    data = {"enable":capture.status()}
    return jsonify(data)

@app.get('/faces_description')
def get_faces_description():
    info = db.get_all_faces_info()
    for f in info:
        f["img"]=f"http://127.0.0.1:5000/get_face_image?id={f['id']}"
        f['display']=False
    return jsonify(info)

@app.get('/get_face_image')
def get_face_image():
    param = request.args.get('id', default=None, type=str)
    if param:
        img = db.get_face_img(param)
        if img: 
            return Response(img, content_type="image/jpeg")
    return ""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
