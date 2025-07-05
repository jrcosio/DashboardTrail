import flet as ft
import cv2
import numpy as np
import time
import threading
from PIL import Image
import io
import base64
from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="./modelosIA/dorsalesYolo11s.pt"):
        self.model = YOLO(model_path)
        self.previous_centroids = {}  # Para trackear cruces de línea
    
    def _point_line_side(self, px, py, x1, y1, x2, y2):
        """Determina en qué lado de la línea está el punto"""
        return (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
    
    def _extract_bbox_image(self, frame, x1, y1, x2, y2):
        """Extrae la imagen del bounding box"""
        return frame[y1:y2, x1:x2]
    
    def detect_and_draw(self, frame, line_coords=None, on_line_cross=None):
        # Hacer inferencia
        results = self.model(frame, classes=[0], conf=0.65)  # Solo clase 0
        
        # Dibujar bounding boxes y detectar cruces
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for i, box in enumerate(boxes):
                    # Coordenadas del bounding box
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    confidence = box.conf[0].cpu().numpy()
                    
                    # Calcular centroide
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    
                    # Dibujar centroide
                    cv2.circle(frame, (cx, cy), 2, (255, 255, 0), -1)
                    
                    # Detectar cruce de línea
                    if line_coords and on_line_cross:
                        current_side = self._point_line_side(cx, cy, line_coords[0], 
                                                           line_coords[1], line_coords[2], line_coords[3])
                        
                        if i in self.previous_centroids:
                            prev_side = self.previous_centroids[i]
                            # Si cambió de lado, cruzó la línea
                            if (prev_side > 0 and current_side < 0) or (prev_side < 0 and current_side > 0):
                                bbox_image = self._extract_bbox_image(frame, x1, y1, x2, y2)
                                on_line_cross(bbox_image)
                        
                        self.previous_centroids[i] = current_side
                    
                    # Dibujar rectángulo
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    
                    # Dibujar confianza
                    label = f"Dorsal: {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1-5), 
                              cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        
        return frame

class Camara:
    def __init__(self, width=450, height=450, line_coords=None, on_line_cross_callback=None):
        self.width = width
        self.height = height
        self.running = True
        self.line_coords = line_coords  # (x1, y1, x2, y2)
        self.on_line_cross_callback = on_line_cross_callback
        self.yolo_detector = YoloDetector()
        
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
    
    def set_line_coords(self, x1, y1, x2, y2):
        """Configura las coordenadas de la línea en tiempo real"""
        self.line_coords = (x1, y1, x2, y2)
    
    def set_line_cross_callback(self, callback):
        """Configura el callback para cuando se cruza la línea"""
        self.on_line_cross_callback = callback
  
    def capture_video(self, page):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return
            
        while self.running:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Aplicar detección YOLO en frame ORIGINAL (sin línea)
            frame_with_detections = self.yolo_detector.detect_and_draw(
                frame.copy(), self.line_coords, self.on_line_cross_callback
            )
            
            # Dibujar línea de meta DESPUÉS (responsabilidad de Camara)
            if self.line_coords:
                cv2.line(frame_with_detections, (self.line_coords[0], self.line_coords[1]), 
                        (self.line_coords[2], self.line_coords[3]), (255, 0, 0), 3)
            
            rgb_frame = cv2.cvtColor(frame_with_detections, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            self.img.src_base64 = img_str
            page.update()
            time.sleep(0.03)  # ~30 FPS
            
        cap.release()



if __name__ == "__main__":
    print("Este módulo no está diseñado para ejecutarse directamente.")