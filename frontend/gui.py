import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import threading
import requests
import json
import csv
from datetime import datetime
from detector import detect_vehicles

with open('config.json') as f:
    config = json.load(f)

class TrafficAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 AI Traffic Analyzer")
        self.image = None
        self.green_signal_time = 0
        self.video_capture = None
        self.running = False
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self.root, text="📷 Load Image", command=self.load_image).pack()
        ttk.Button(self.root, text="🎥 Start Camera", command=self.start_camera).pack()
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if path:
            image = cv2.imread(path)
            self.process_frame(image)

    def start_camera(self):
        self.video_capture = cv2.VideoCapture(0)
        self.running = True
        threading.Thread(target=self.process_video).start()

    def process_video(self):
        while self.running:
            ret, frame = self.video_capture.read()
            if not ret:
                break
            self.process_frame(frame)
        self.video_capture.release()

    def process_frame(self, frame):
        vehicle_count, annotated = detect_vehicles(frame)
        self.green_signal_time = self.get_green_time(vehicle_count)
        img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.canvas.image = img_tk
        self.save_to_csv(vehicle_count, self.green_signal_time)

    def get_green_time(self, count):
        try:
            resp = requests.post(config['flask_url'], json={"vehicle_count": count}, timeout=5)
            return resp.json().get('green_signal_time', 20)
        except:
            return min(max(count * 3, 10), 60)

    def save_to_csv(self, count, green_time):
        with open("traffic_log.csv", mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), count, green_time])

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficAnalyzerApp(root)
    root.mainloop()
