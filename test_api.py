import cv2
import numpy as np
import base64
from app import app

client = app.test_client()

# Create dummy RGB image with a painted face-like shape
img = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.circle(img, (320, 240), 90, (200, 180, 150), -1)

# Encode to base64
_, buffer = cv2.imencode('.jpg', img)
b64_str = f"data:image/jpeg;base64,{base64.b64encode(buffer).decode('utf-8')}"

filters_to_test = [
    'dog', 'shades', 'crown', 'anime', 'devil', 'laser', 'glitch', 'bw', 'inverted', 'neon', 'none'
]

for f in filters_to_test:
    res = client.post('/api/process_frame', json={'image': b64_str, 'filter': f})
    assert res.status_code == 200, f"Failed on filter {f}: {res.status_code}"
    data = res.get_json()
    assert 'image' in data and data['image'].startswith('data:image/jpeg;base64,'), f"Invalid output on {f}"
    print(f"Filter [{f}] passed test successfully.")

print("All 11 fun filters passed test suite!")
