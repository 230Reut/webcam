from flask import Flask, flash, redirect, render_template, Response, request, session, url_for, jsonify, send_file
from flask_cors import CORS
import cv2
import io
from datetime import datetime
from login import *


events_log = []

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


# Notify
@app.route('/record_who_went', methods=['POST'])
def record_who_went():
    
    data = request.get_json()
    
    # Check for display name, time and gender
    display_name = data.get('display_name', 'Unknown')

    #Create log message
    time_stamp = datetime.now().strftime("%H:%M:%S")
    message = f'{display_name} {time_stamp}'
    
    # Log to today's logfile
    file_name =  f'./logs/{datetime.now().strftime("%d-%m-%y")}.txt'
    with open(file_name, "a", encoding='utf-8') as log_file:
        log_file.write(message + '\n')

    # Return all logs to frontend 
    events_log.insert(0, message)
    return jsonify({'message':message})


# Get all notification
@app.route('/get_events_log', methods=['GET'])
def get_events_log():
    # Display only last 10 logs
    return jsonify({'events': events_log[:10]})


def generate_frames():
    while True:
        # Read frame from the webcam
        success, frame = video_capture.read()  
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
