import flet as ft
import cv2
import numpy as np
import time
import threading
from PIL import Image
import io
import base64

class Camara:
    def __init__(self, width=450, height=450):
        self.width = width
        self.height = height
        self.running = True  # Siempre activa

        # Crear contenedor de video
        self.video_container = ft.Container(
            width=self.width,
            height=self.height,
            border=ft.border.all(2, ft.Colors.WHITE),
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

    def build(self):
        return ft.Column([
            # ft.Text('Prueba de OpenCV con Flet Proyecto David', size=24, weight="bold"),
            self.video_container,
        ], alignment=ft.MainAxisAlignment.CENTER)

    def capture_video(self, page):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            self.img.src_base64 = img_str
            page.update()
            time.sleep(0.03)  # ~30 FPS

        cap.release()

def main(page: ft.Page):
    page.title = "Flet + OpenCV Video"
    page.padding = 20
    page.theme_mode = "dark"

    camara = Camara()
    page.add(camara.build())

    # Iniciar la cámara automáticamente en un hilo
    threading.Thread(target=camara.capture_video, args=(page,), daemon=True).start()

ft.app(target=main)