from flask import Flask, request, jsonify
import cv2
import base64

app = Flask(__name__)

@app.route('/video_frames', methods=['POST','GET'])
def get_video_frames():
    try:
        video_path = request.json.get('video_path')

        # Check if video path is provided
        if not video_path:
            return jsonify({'error': 'Video path is required'}), 400

        # Open the video file
        video = cv2.VideoCapture(video_path)

        # Check if video file is valid
        if not video.isOpened():
            return jsonify({'error': 'Unable to open video file'}), 400

        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = int(total_frames / fps)
        
        # Extract frames
        frames = []
        for i in range(duration):
            frame_id = int(fps * i)
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = video.read()
            if ret:
                success, frame_bytes = cv2.imencode('.jpg', frame)
                if success:
                    frames.append(base64.b64encode(frame_bytes).decode('utf-8'))

        # Release video capture object
        video.release()

        

        return jsonify({'frames': frames}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
