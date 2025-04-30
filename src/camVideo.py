import cv2
import threading
from flask import Flask, Response, render_template_string, request

app = Flask(__name__)
cam_event = threading.Event()
stop_event = threading.Event()

with open('page.html', 'r') as file:
    HTML = file.read() 

def generate_frames():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return
    while not stop_event.is_set():
        if cam_event.is_set():
            ret,frame = cap.read()
            
            if not ret:
                print('error during camera data retrieve')
                break

            _, buffer = cv2.imencode('.jpg',frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            threading.Event().wait(0.1)

    cap.release()
    print("Camera released.")

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/start')
def start_camera():
    cam_event.set()
    return '', 204

@app.route('/stop')
def stop_camera():
    cam_event.clear()
    return '', 204

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    app.run(host='0.0.0.0', port=5000, threaded=True)

if __name__ == "__main__":
    main()
