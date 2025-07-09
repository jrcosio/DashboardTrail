import threading
from typing import Callable
from datetime import datetime
import os


class Terminal:
    """Clase súper simple para agregar terminal a cualquier app Flet."""
    
    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback
        self.running = False
    
    def start(self):
        """Iniciar terminal."""
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()
        print("🟢 Terminal iniciado. Escribe 'quit' para cerrar.")
    
    def _loop(self):
        """Bucle del terminal."""
        while self.running:
            try:
                msg = input("Dorsal> ").strip()
                if msg.lower() == 'quit':
                    self.running = False
                    break
                if msg:
                    self.callback(msg)
            except (EOFError, KeyboardInterrupt):
                self.running = False
                break
            
# import flet as ft
# def main(page: ft.Page):
#     page.title = "Super Simple Terminal"
    
#     # Solo un texto que se actualiza
#     texto = ft.Text("Escribe algo en el terminal", size=16)
#     page.add(texto)
    
#     # Callback que actualiza el texto
#     def actualizar_texto(mensaje):
#         texto.value = f"Último mensaje: {mensaje}"
#         page.update()
    
#     # Crear e iniciar terminal en una línea
#     Terminal(actualizar_texto).start()


# if __name__ == "__main__":
#     ft.app(target=main)            
    
 