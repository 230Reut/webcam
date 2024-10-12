from flask import Flask, flash, redirect, render_template, Response, request, session, url_for, jsonify, send_file
from flask_cors import CORS
import cv2
import io
from datetime import datetime
from login import *



# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Main page to view the stream (Login required)
@app.route('/')
def index():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    display_name = session.get('display_name')
    return render_template('index.html', display_name=display_name) 

# Video feed route (Login required)
@app.route('/video_feed')
def video_feed():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Snapshot
@app.route('/take_shot', methods=['GET'])
def take_shot():
    
    # Capture frame 
    success, frame = video_capture.read()
    if not success:
        return jsonify({"success": False}), 500

    # Encode to JPEG
    _, buffer = cv2.imencode('.jpg', frame)

    # Create a bytes stream to send the img as a file-like object
    img_io = io.BytesIO(buffer)

    #Save img
    time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"snapshot_{time_stamp}.jpg"

    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name=file_name)

def generate_frames():
    while True:
        success, frame = video_capture.read()  # Read frame from the webcam
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Yield the frame to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
