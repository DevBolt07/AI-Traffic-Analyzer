# 🚦 AI-Powered Traffic Image & Video Analyzer

An end-to-end traffic analysis system that uses YOLOv8 for robust vehicle detection and a modern Tkinter desktop UI for image/video visualization and green-signal-time (GST) suggestions. Backend API (Flask) computes GST and the frontend provides both image and video workflows with live annotated previews.

---

## 🔥 Highlights (latest updates)

- YOLOv8-based detector (ultralytics) — detects cars, trucks, buses, motorcycles, pedestrians.
- Flask backend with `/process` endpoint for green-signal-time calculation.
- Modern Tkinter desktop UIs:
  - Image analyzer (styled, with countdown/timer controls).
  - Video analyzer (live frame-by-frame detection with annotated preview).
- Video processing: select video file → optionally start detection → live annotated frames and per-frame vehicle counts.
- CSV logging of detections and recommended GST.
- Styled UI color grading and consistent look across apps.

---

## 📁 Project structure (important files)

- backend/
  - app.py — Flask API (POST /process) returns green_signal_time
- frontend/
  - detector.py — YOLOv8 integration and annotate frames
  - gui.py — image analyzer UI (styled, countdown/progress)
  - vid_det.py — modern video analyzer UI (styled, live preview)
  - requirements.txt — Python dependencies
  - config.json — model path, thresholds, Flask URL (used by detector and GUI)
  - traffic_log.csv — detection log (appends runtime results)
  - yolov8n.pt — model weights (DO NOT commit large models to GitHub)

---

## ⚙️ Requirements

- Python 3.8+
- Install deps:
  - pip install -r frontend/requirements.txt
  - Ensure `ultralytics`, `opencv-python`, `pillow`, `flask`, `requests` are installed
- Place YOLOv8 weights (e.g., yolov8n.pt) in `frontend/` and set `config.json` correctly.

---

## ▶ Quick start

1. Start backend (detection / GST API):
   - cd backend
   - python app.py
   - Flask runs on http://localhost:5000 by default

2. Run Image Analyzer UI:
   - python frontend/gui.py
   - Upload an image → analysis runs → annotation, GST suggestion and countdown.

3. Run Video Analyzer UI:
   - python frontend/vid_det.py
   - Choose a video file. Click `Start Detecting` to process the selected video. (UI also supports auto-start behavior if desired.)

Note: `gui.py` also supports webcam mode (Start Camera) which streams frames to the detector.

---

## 🧠 Detector behavior

- Uses ultralytics.YOLO model loaded from `config.json` (`model_path`).
- Filtering: detects objects and counts classes ["car", "truck", "bus", "motorbike"] (configurable).
- Returns annotated frames (bounding boxes + labels) and per-frame vehicle counts.
- Typical YOLOv8 console output (per-frame inference time) will appear when running detection.

---

## ⏱ GST (Green Signal Time) logic

- Backend `app.py` currently computes GST from vehicle count and emergency flag:
  - emergency → 40s
  - <=2 vehicles → 10s
  - 3–5 vehicles → 20s
  - >5 vehicles → 30s
- Frontend GUIs display suggested GST and provide a countdown/progress UI.
- Recommended: replace backend logic with PCU/queue-based formula for per-lane adaptive GST (see project notes).

---

## 📊 Logging & persistence

- Detection events are appended to `frontend/traffic_log.csv` with timestamp, vehicle_count, and green_time.
- Use logs to calibrate PCU values and refine GST formulas.

---

## 🛠 Troubleshooting

- Large files on GitHub:
  - Do not commit large videos or model weights. Use .gitignore or Git LFS.
  - Remove large files from staged commits if needed:
    - git rm --cached <file>
    - commit and push
- FFmpeg / OpenCV warning:
  - `Assertion fctx->async_lock failed at libavcodec/pthread_frame.c:173` — FFmpeg threading warning from OpenCV/FFmpeg during decode. If app runs correctly, this can be ignored. Convert video to a standard H.264 mp4 if you see crashes.
- If the detector does not detect bikes:
  - Confirm `detector.py` class mapping and `model.names`. Official YOLOv8 models pretrained on COCO include `bicycle` and `motorcycle`.
  - You can print `model.names` or check `config.json`.

---

## ✅ UI behavior notes

- Image analyzer: styled panels, upload, analysis, GST suggestion, countdown.
- Video analyzer (`vid_det.py`):
  - Choose video → UI enables `Start Detecting` button.
  - Click `Start Detecting` → stops previous display and processes selected video (live annotated preview + results).
  - Emergency Override expands green time to 40s and updates status.

---

## 📌 Tips & next steps

- Replace simple GST logic with PCU-weighted, queue-aware formula using YOLOv8 class, bbox size, and temporal tracking.
- Add WebSocket streaming for real-time frontend-backend integration.
- Persist detections in SQLite for efficient analytics.
- Add authentication and package into Docker for deployment.

---

## Contributing

- Open an issue or PR for features or bug fixes.
- Keep large binaries out of the repo; use cloud storage or Git LFS.

---



