import flet as ft
import cv2
import numpy as np
import time
import threading
from PIL import Image
import io
import base64

def main(page: ft.Page):
    page.title = "Flet + OpenCV Video"
    page.padding = 20
    page.theme_mode = "dark"
    
    # Crear un contenedor para mostrar el video
    video_container = ft.Container(
        width=800,
        height=600,
        border=ft.border.all(2, ft.Colors.WHITE),
        border_radius=ft.border_radius.all(10),
        alignment=ft.alignment.center,
    )
    
    # Imagen para mostrar frames de video
    img = ft.Image(
        width=800,
        height=600,
        fit=ft.ImageFit.CONTAIN,
    )
    video_container.content = img
    
    # Variable para controlar la captura de video
    running = True
    
    def capture_video():
        # Iniciar la cámara web
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: No se pudo abrir la cámara.")
            return
            
        while running:
            # Capturar frame
            ret, frame = cap.read()
            if not ret:
                break
                
            # Opcional: Aplicar algún procesamiento de OpenCV
            # Por ejemplo, convertir a escala de grises y luego de vuelta a BGR
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            # Convertir de BGR a RGB (OpenCV usa BGR, PIL usa RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convertir a imagen PIL
            pil_img = Image.fromarray(rgb_frame)
            
            # Convertir a base64 para mostrar en Flet
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # Actualizar la imagen en la UI de Flet
            img.src_base64 = img_str
            
            # Actualizar la UI (debe hacerse en el hilo principal)
            page.update()
            
            # Agregar un pequeño retraso para no saturar la CPU
            time.sleep(0.03)  # ~30 FPS
            
        # Liberar la cámara cuando termine
        cap.release()
    
    # Botones para controlar la cámara
    def start_video(e):
        nonlocal running
        running = True
        # Iniciar captura en un hilo separado
        threading.Thread(target=capture_video, daemon=True).start()
        start_btn.disabled = True
        stop_btn.disabled = False
        page.update()
    
    def stop_video(e):
        nonlocal running
        running = False
        start_btn.disabled = False
        stop_btn.disabled = True
        page.update()
    
    start_btn = ft.ElevatedButton("Iniciar Cámara", on_click=start_video)
    stop_btn = ft.ElevatedButton("Detener Cámara", on_click=stop_video, disabled=True)

    
    # Añadir controles a la página
    page.add(
        ft.Column([
            ft.Text('Prueba de OpenCV con Flet Proyecto David', size=24, weight="bold"),
            video_container,
            ft.Row([
                start_btn, 
                stop_btn,
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)