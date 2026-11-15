import cv2
import numpy as np

def overlay_transparent(background, overlay, x, y, overlay_size=None):
    """
    Overlays a 4-channel PNG (RGBA) onto a 3-channel background BGR image with alpha blending.
    Safely clips bounds to prevent indexing errors near image borders.
    """
    if overlay is None or overlay.shape[2] != 4:
        return background

    if overlay_size is not None:
        w, h = overlay_size
        if w <= 0 or h <= 0:
            return background
        overlay = cv2.resize(overlay, (w, h), interpolation=cv2.INTER_AREA)

    h, w = overlay.shape[:2]
    bg_h, bg_w = background.shape[:2]

    # Calculate clipping boundaries
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(bg_w, x + w), min(bg_h, y + h)

    if x1 >= x2 or y1 >= y2:
        return background

    # Overlay slice
    ox1, oy1 = x1 - x, y1 - y
    ox2, oy2 = ox1 + (x2 - x1), oy1 + (y2 - y1)

    overlay_crop = overlay[oy1:oy2, ox1:ox2]
    bg_crop = background[y1:y2, x1:x2]

    # Normalize alpha channel (0.0 to 1.0)
    alpha = (overlay_crop[:, :, 3] / 255.0)[:, :, np.newaxis]
    overlay_bgr = overlay_crop[:, :, :3]

    # Alpha composite
    composite = (alpha * overlay_bgr + (1.0 - alpha) * bg_crop).astype(np.uint8)
    background[y1:y2, x1:x2] = composite
    return background


class FaceFilterEngine:
    def __init__(self):
        # Load Haar Cascades for face and eye detection
        cascade_path = cv2.data.haarcascades
        self.face_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cascade_path + 'haarcascade_eye.xml')

        # Load transparent overlay assets
        self.dog_ear_left = cv2.imread('static/filters/dog_ear_left.png', cv2.IMREAD_UNCHANGED)
        self.dog_ear_right = cv2.imread('static/filters/dog_ear_right.png', cv2.IMREAD_UNCHANGED)
        self.dog_nose = cv2.imread('static/filters/dog_nose.png', cv2.IMREAD_UNCHANGED)
        
        self.pixel_shades = cv2.imread('static/filters/pixel_shades.png', cv2.IMREAD_UNCHANGED)
        self.crown = cv2.imread('static/filters/crown.png', cv2.IMREAD_UNCHANGED)
        
        self.cat_ear_left = cv2.imread('static/filters/cat_ear_left.png', cv2.IMREAD_UNCHANGED)
        self.cat_ear_right = cv2.imread('static/filters/cat_ear_right.png', cv2.IMREAD_UNCHANGED)
        self.anime_blush = cv2.imread('static/filters/anime_blush.png', cv2.IMREAD_UNCHANGED)
        
        self.devil_horn_left = cv2.imread('static/filters/devil_horn_left.png', cv2.IMREAD_UNCHANGED)
        self.devil_horn_right = cv2.imread('static/filters/devil_horn_right.png', cv2.IMREAD_UNCHANGED)

    def detect_faces(self, gray_frame):
        return self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(80, 80)
        )

    def apply_filter(self, frame, filter_type='none'):
        if filter_type == 'none':
            return frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detect_faces(gray)

        # 1. Classic Dog Snap Filter
        if filter_type == 'dog':
            result = frame.copy()
            for (x, y, w, h) in faces:
                ear_w = int(w * 0.48)
                ear_h = int(h * 0.65)
                # Left ear
                overlay_transparent(result, self.dog_ear_left, int(x - ear_w * 0.3), int(y - ear_h * 0.65), (ear_w, ear_h))
                # Right ear
                overlay_transparent(result, self.dog_ear_right, int(x + w - ear_w * 0.7), int(y - ear_h * 0.65), (ear_w, ear_h))
                # Nose & Tongue
                nose_w = int(w * 0.52)
                nose_h = int(h * 0.42)
                nose_x = int(x + (w - nose_w) / 2)
                nose_y = int(y + h * 0.48)
                overlay_transparent(result, self.dog_nose, nose_x, nose_y, (nose_w, nose_h))
            return result

        # 2. Pixel Sunglasses (Thug Life / Deal With It)
        elif filter_type == 'shades':
            result = frame.copy()
            for (x, y, w, h) in faces:
                shades_w = int(w * 0.95)
                shades_h = int(h * 0.38)
                shades_x = int(x + (w - shades_w) / 2)
                shades_y = int(y + h * 0.28)
                overlay_transparent(result, self.pixel_shades, shades_x, shades_y, (shades_w, shades_h))
            return result

        # 3. Gold Royalty Crown
        elif filter_type == 'crown':
            result = frame.copy()
            for (x, y, w, h) in faces:
                crown_w = int(w * 0.85)
                crown_h = int(h * 0.55)
                crown_x = int(x + (w - crown_w) / 2)
                crown_y = int(y - crown_h * 0.78)
                overlay_transparent(result, self.crown, crown_x, crown_y, (crown_w, crown_h))
            return result

        # 4. Cute Anime Cat Girl / Neko
        elif filter_type == 'anime':
            result = frame.copy()
            for (x, y, w, h) in faces:
                # Cat ears
                ear_size = int(w * 0.42)
                overlay_transparent(result, self.cat_ear_left, int(x - ear_size * 0.15), int(y - ear_size * 0.7), (ear_size, ear_size))
                overlay_transparent(result, self.cat_ear_right, int(x + w - ear_size * 0.85), int(y - ear_size * 0.7), (ear_size, ear_size))
                # Cheeks blush
                blush_w = int(w * 0.28)
                blush_h = int(h * 0.18)
                # Left cheek
                overlay_transparent(result, self.anime_blush, int(x + w * 0.08), int(y + h * 0.58), (blush_w, blush_h))
                # Right cheek
                overlay_transparent(result, self.anime_blush, int(x + w * 0.64), int(y + h * 0.58), (blush_w, blush_h))
            return result

        # 5. Devil Horns & Red Aura
        elif filter_type == 'devil':
            # Slight dark red aesthetic tint
            b, g, r = cv2.split(frame)
            r = cv2.add(r, 20)
            result = cv2.merge([b, g, r])
            for (x, y, w, h) in faces:
                horn_w = int(w * 0.32)
                horn_h = int(h * 0.45)
                overlay_transparent(result, self.devil_horn_left, int(x + w * 0.08), int(y - horn_h * 0.65), (horn_w, horn_h))
                overlay_transparent(result, self.devil_horn_right, int(x + w * 0.60), int(y - horn_h * 0.65), (horn_w, horn_h))
            return result

        # 6. Laser / Alien Eyes (Viral glow)
        elif filter_type == 'laser':
            result = frame.copy()
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + int(h * 0.65), x:x + w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4, minSize=(25, 25))
                
                # If eyes found via cascade, shoot lasers from exact pupil coordinates; else estimate from face
                laser_points = []
                if len(eyes) >= 2:
                    for (ex, ey, ew, eh) in eyes[:2]:
                        laser_points.append((x + ex + ew // 2, y + ey + eh // 2))
                else:
                    laser_points = [(x + int(w * 0.32), y + int(h * 0.38)), (x + int(w * 0.68), y + int(h * 0.38))]

                for (lx, ly) in laser_points:
                    # Laser flares / radial glow
                    for radius, color in [(35, (0, 0, 255)), (22, (0, 140, 255)), (12, (100, 255, 255)), (5, (255, 255, 255))]:
                        cv2.circle(result, (lx, ly), radius, color, -1)
                    # Intense laser blast lines shooting forward
                    cv2.line(result, (lx, ly), (lx - 80, result.shape[0]), (0, 80, 255), 6)
                    cv2.line(result, (lx, ly), (lx - 80, result.shape[0]), (255, 255, 255), 2)
            return result

        # 7. Retro VHS / Glitch Filter
        elif filter_type == 'glitch':
            b, g, r = cv2.split(frame)
            # Chromatic aberration channel shifting
            shift = 12
            r_shifted = np.roll(r, shift, axis=1)
            b_shifted = np.roll(b, -shift, axis=1)
            glitched = cv2.merge([b_shifted, g, r_shifted])
            # Scanlines overlay
            scanlines = np.zeros_like(frame)
            scanlines[::4, :, :] = 45
            glitched = cv2.subtract(glitched, scanlines)
            return glitched

        # 8. Black and White Filter
        elif filter_type == 'bw':
            bw = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            bw = cv2.convertScaleAbs(bw, alpha=1.2, beta=-5)
            for (x, y, w, h) in faces:
                cv2.rectangle(bw, (x, y), (x + w, y + h), (220, 220, 220), 2)
            return bw

        # 9. Inverted (Negative)
        elif filter_type == 'inverted':
            inverted = cv2.bitwise_not(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(inverted, (x, y), (x + w, y + h), (0, 255, 255), 2)
            return inverted

        # 10. Cyberpunk / Neon Glow
        elif filter_type == 'neon':
            edges = cv2.Canny(gray, 60, 150)
            edges_dilated = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)
            glow = np.zeros_like(frame)
            glow[edges_dilated > 0] = [255, 0, 210]  # Hot pink
            blended = cv2.addWeighted(frame, 0.45, glow, 0.85, 0)
            for (x, y, w, h) in faces:
                cv2.rectangle(blended, (x, y), (x + w, y + h), (0, 255, 255), 2)
            return blended

        return frame
