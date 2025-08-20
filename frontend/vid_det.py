import cv2
from detector import detect_vehicles
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading

class ModernTrafficAnalyzerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚦 Traffic Video Analyzer")
        self.root.geometry("1200x900")
        self.root.configure(bg='#f8f9fa')
        self.root.state('zoomed')
        self.video_path = None
        self.cap = None
        self.running = False
        self.green_signal_time = 0

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), background='#f8f9fa', foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 11), background='#f8f9fa', foreground='#7f8c8d')
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'), background='#f8f9fa', foreground='#34495e')
        style.configure('Info.TLabel', font=('Segoe UI', 11), background='#f8f9fa', foreground='#5d6d7e')
        style.configure('Success.TLabel', font=('Segoe UI', 12, 'bold'), background='#f8f9fa', foreground='#27ae60')
        style.configure('Countdown.TLabel', font=('Segoe UI', 28, 'bold'), background='#f8f9fa', foreground='#e74c3c')
        style.configure('Custom.TButton', font=('Segoe UI', 11, 'bold'), background='#3498db', foreground='white', padding=(15, 10))
        style.configure('Emergency.TButton', font=('Segoe UI', 11, 'bold'), background='#e74c3c', foreground='white', padding=(15, 10))
        style.map('Emergency.TButton',
                  background=[('active', '#c0392b'), ('!active', '#e74c3c')],
                  foreground=[('active', 'white'), ('!active', 'white')])

    def create_widgets(self):
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Header
        header_frame = tk.Frame(main_container, bg='#f8f9fa', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        title_label = ttk.Label(header_frame, text="🚦 Traffic Video Analyzer", style='Title.TLabel')
        title_label.pack(pady=(10, 5))
        subtitle_label = ttk.Label(header_frame, text="AI-Powered Traffic Density Analysis & Signal Management",
                                  style='Subtitle.TLabel')
        subtitle_label.pack()

        # Content area
        content_frame = tk.Frame(main_container, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Video and Upload
        left_column = tk.Frame(content_frame, bg='#f8f9fa')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Upload section
        upload_frame = ttk.LabelFrame(left_column, text="  📁 Video Upload  ", padding=15)
        upload_frame.pack(fill=tk.X, pady=(0, 15))
        self.upload_button = ttk.Button(upload_frame, text="📂 Choose Traffic Video",
                                        command=self.select_video, style='Custom.TButton')
        self.upload_button.pack()

        # Start Detecting button
        self.start_button = ttk.Button(upload_frame, text="▶ Start Detecting",
                                       command=self.start_detection, style='Custom.TButton', state="disabled")
        self.start_button.pack(pady=(10, 0))

        # Video display section
        video_frame = ttk.LabelFrame(left_column, text="  🎥 Video Analysis  ", padding=15)
        video_frame.pack(fill=tk.BOTH, expand=True)
        self.video_canvas = tk.Canvas(video_frame, bg='white', relief=tk.SUNKEN, bd=2, height=500)
        self.video_canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas_text = self.video_canvas.create_text(
            400, 250,
            text="🎬\n\nNo Video Selected\n\nClick 'Choose Traffic Video' to upload a video for analysis",
            font=('Segoe UI', 14),
            fill='#95a5a6',
            justify=tk.CENTER
        )

        # Right column - Results and Controls
        right_column = tk.Frame(content_frame, bg='#f8f9fa', width=400)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_column.pack_propagate(False)

        # Results section
        results_frame = ttk.LabelFrame(right_column, text="  📊 Analysis Results  ", padding=20)
        results_frame.pack(fill=tk.X, pady=(0, 15))
        self.result_label = ttk.Label(results_frame,
                                      text="No analysis performed yet.\nUpload a video to begin.",
                                      style='Info.TLabel', justify=tk.CENTER)
        self.result_label.pack(pady=10)
        self.vehicle_count_label = ttk.Label(results_frame,
                                             text="Vehicles Detected: 0",
                                             font=('Segoe UI', 20, 'bold'),
                                             foreground="#388e3c")
        self.vehicle_count_label.pack(pady=5)
        self.green_time_label = ttk.Label(results_frame,
                                          text="Green Time: --",
                                          font=('Segoe UI', 14),
                                          foreground="#1976d2")
        self.green_time_label.pack(pady=5)
        self.traffic_density_label = ttk.Label(results_frame,
                                               text="Traffic Density: --",
                                               font=('Segoe UI', 14),
                                               foreground="#388e3c")
        self.traffic_density_label.pack(pady=5)

        # Action buttons section
        action_frame = ttk.LabelFrame(right_column, text="  ⚡ Actions  ", padding=20)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        self.emergency_button = ttk.Button(action_frame, text="🚨 Emergency Override",
                                           command=self.handle_emergency, style='Emergency.TButton')
        self.emergency_button.pack(fill=tk.X)

        # Countdown section
        countdown_frame = ttk.LabelFrame(right_column, text="  ⏱️ Traffic Light Timer  ", padding=20)
        countdown_frame.pack(fill=tk.BOTH, expand=True)
        self.countdown_label = ttk.Label(countdown_frame, text="", style='Countdown.TLabel')
        self.countdown_label.pack(pady=(20, 15))
        self.progress = ttk.Progressbar(countdown_frame, mode='determinate', length=300)
        self.progress.pack(fill=tk.X, pady=(0, 15))
        self.progress.pack_forget()
        self.status_label = ttk.Label(countdown_frame, text="", style='Info.TLabel', justify=tk.CENTER)
        self.status_label.pack()

        # Bottom info section
        info_frame = tk.Frame(right_column, bg='#ecf0f1', relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=(15, 0))
        info_text = tk.Label(info_frame,
                             text="💡 Tips:\n• Use clear traffic videos\n• Ensure good lighting\n• Multiple vehicles work best",
                             font=('Segoe UI', 9), bg='#ecf0f1', fg='#34495e', justify=tk.LEFT)
        info_text.pack(pady=10, padx=10)

    def select_video(self):
        path = filedialog.askopenfilename(
            title="Select Traffic Video for Analysis",
            filetypes=[
                ("Video Files", "*.mp4 *.avi *.mov *.mkv"),
                ("All files", "*.*")
            ]
        )
        if path:
            self.video_path = path
            self.result_label.config(text="Video selected. Click 'Start Detecting' to begin.", style='Info.TLabel')
            self.start_button.config(state="normal")
            self.running = False  # Stop any previous detection

    def start_detection(self):
        if not self.video_path:
            return
        self.running = False  # Stop any previous detection
        self.result_label.config(text="🔄 Processing video...\nPlease wait...", style='Info.TLabel')
        self.vehicle_count_label.config(text="Vehicles Detected: 0")
        self.green_time_label.config(text="Green Time: --")
        self.traffic_density_label.config(text="Traffic Density: --", foreground="#388e3c")
        self.video_canvas.delete("all")
        self.canvas_text = self.video_canvas.create_text(
            400, 250,
            text="Detecting...",
            font=('Segoe UI', 18, 'bold'),
            fill='#95a5a6',
            justify=tk.CENTER
        )
        self.running = True
        threading.Thread(target=self.process_video, daemon=True).start()

    def process_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
        frame_idx = 0
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            vehicle_count, annotated = detect_vehicles(frame)
            self.vehicle_count_label.config(text=f"Vehicles Detected: {vehicle_count}")

            # Example green time logic
            if vehicle_count <= 2:
                green_time = 10
                density = "Low"
                color = "#388e3c"
            elif vehicle_count <= 5:
                green_time = 20
                density = "Medium"
                color = "#ffa000"
            else:
                green_time = 30
                density = "High"
                color = "#e74c3c"

            self.green_time_label.config(text=f"Green Time: {green_time}s")
            self.traffic_density_label.config(text=f"Traffic Density: {density}", foreground=color)
            self.result_label.config(text="Analysis Complete!", style='Success.TLabel')

            # Update timer bar
            self.progress["maximum"] = green_time
            self.progress["value"] = min(frame_idx % green_time, green_time)
            self.countdown_label.config(text=f"{green_time}s")

            # Convert frame for Tkinter display
            img_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_pil = img_pil.resize((800, 500))
            img_tk = ImageTk.PhotoImage(img_pil)

            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.video_canvas.image = img_tk

            frame_idx += 1
            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.cap.release()
        self.result_label.config(text="Processing complete.", style='Success.TLabel')

    def handle_emergency(self):
        self.green_signal_time = 40
        emergency_text = f"🚨 EMERGENCY OVERRIDE!\n\n⚠️ Priority vehicle detected\n⏱️ Extended time: {self.green_signal_time}s\n\n🚑 Emergency protocols active"
        self.result_label.config(text=emergency_text, style='Success.TLabel')
        self.countdown_label.config(text=f"{self.green_signal_time}")
        self.progress["maximum"] = self.green_signal_time
        self.progress["value"] = self.green_signal_time
        self.status_label.config(text="🛑 Emergency Mode", foreground='#e74c3c')

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = ModernTrafficAnalyzerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()