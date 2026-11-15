import base64
import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
from filter_engine import FaceFilterEngine

app = Flask(__name__)
engine = FaceFilterEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({'error': 'Invalid request payload'}), 400

        filter_name = data.get('filter', 'none')
        image_data = data['image']

        # Parse base64 data URL
        if ',' in image_data:
            image_data = image_data.split(',', 1)[1]

        # Decode JPEG into NumPy OpenCV BGR image
        image_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Failed to decode image buffer'}), 400

        # Apply the selected computer vision filter
        processed_frame = engine.apply_filter(frame, filter_name)

        # Encode back to JPEG
        success, encoded_img = cv2.imencode('.jpg', processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not success:
            return jsonify({'error': 'Failed to encode processed frame'}), 500

        result_b64 = base64.b64encode(encoded_img).decode('utf-8')
        return jsonify({'image': f'data:image/jpeg;base64,{result_b64}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 VisionFilter AI Studio starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
