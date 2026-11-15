# VisionFilter AI Studio 🐶✨

A real-time Computer Vision & Face Filter web application powered by **Python**, **OpenCV**, and **Flask**.

## 🚀 Features

- **Real-Time Web Webcam Processing**: Captures live video feed in the browser with zero external plugins.
- **AI Face Detection**: Uses OpenCV Haar Feature-based Cascade Classifiers (`haarcascade_frontalface_default`).
- **Interactive Filters**:
  - 🐶 **Dog Snap**: Custom-rendered floppy dog ears, muzzle, and tongue dynamically mapped and scaled to detected facial coordinates with seamless alpha-blending.
  - 🖤 **Black & White (B&W)**: High-contrast monochrome grading with face boundary highlights.
  - 🌀 **Inverted**: Negative color transformation with cyberpunk face bounds.
  - 🎭 **Face Spotlight**: Grayscale background isolation leaving detected face regions in vivid color.
  - ⚡ **Cyberpunk Neon**: Canny edge detection with glowing magenta outlines.
- **📸 Snapshot Tool**: Save filtered pictures directly to your local computer in 1 click.
- **Performance Monitor**: Real-time FPS and server inference latency stats.

---

## 🛠️ How to Run

1. Open a terminal in this project directory:
   ```bash
   cd "face filter app"
   ```

2. Start the application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```
   Allow camera access when prompted, select any filter, and have fun!
