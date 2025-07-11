import flet as ft
import cv2
import numpy as np
import time
import threading
from PIL import Image
import io
import base64
import os
import warnings
import logging

# Silenciar completamente YOLO
os.environ['YOLO_VERBOSE'] = 'False'
warnings.filterwarnings("ignore")

# Configurar logging de ultralytics para que no muestre nada
logging.getLogger('ultralytics').setLevel(logging.CRITICAL)

from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="./yolo11s.pt"):
        # Cargar el modelo de manera silenciosa
        self.model = YOLO(model_path, verbose=False)
    
    def detect_and_draw(self, frame):
        # Hacer inferencia de manera silenciosa
        results = self.model(frame, classes=[0], verbose=False)  # Solo clase 0
        
        # Dibujar bounding boxes
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Coordenadas del bounding box
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    confidence = box.conf[0].cpu().numpy()
                    
                    # Dibujar rectángulo
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Dibujar confianza
                    label = f"Clase 0: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame

class Camara:
    def __init__(self, width=450, height=450):
        self.width = width
        self.height = height
        self.running = True
        self.yolo_detector = YoloDetector()  # Añadir detector YOLO
        
        # Crear contenedor de video
        self.video_container = ft.Container(
            width=self.width,
            height=self.height,
            border_radius=ft.border_radius.all(10),
            alignment=ft.alignment.center,
        )
        
        # Imagen para mostrar frames de video
        self.img = ft.Image(
            width=self.width,
            height=self.height,
            fit=ft.ImageFit.CONTAIN,
        )
        self.video_container.content = self.img
  
    def capture_video(self, page):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return
            
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Aplicar detección YOLO
            frame_with_detections = self.yolo_detector.detect_and_draw(frame)
            
            rgb_frame = cv2.cvtColor(frame_with_detections, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            self.img.src_base64 = img_str
            page.update()
            time.sleep(0.03)  # ~30 FPS
            
        cap.release()