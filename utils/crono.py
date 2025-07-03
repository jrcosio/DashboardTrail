import flet as ft
from datetime import datetime, timedelta
import threading
import time

class Cronometro(ft.Container):
    def __init__(self, start_time=None, **kwargs):
        """
        Cronómetro para carreras.
        
        Args:
            start_time: datetime - Momento de inicio previo (para recuperar estado)
        """
        super().__init__(**kwargs)
        
        # Estado del cronómetro
        self.start_time = start_time  # None = no iniciado, datetime = iniciado
        self.is_running = False
        self.timer_thread = None
        self.stop_event = threading.Event()
        
        # Estilos
        self.text_style = ft.TextStyle(
            size=190, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.WHITE
        )
        self.label_style = ft.TextStyle(
            size=24, 
            color=ft.Colors.WHITE
        )
        self.box_style = {
            "bgcolor": ft.Colors.BLUE_300,
            "border_radius": 10,
            "padding": 10,
            "width": 300,
            "height": 330,
            "alignment": ft.alignment.center,
        }
        
        # Componentes UI
        self.hours_text = ft.Text("00", style=self.text_style)
        self.minutes_text = ft.Text("00", style=self.text_style)
        self.seconds_text = ft.Text("00", style=self.text_style)
        
        self.hours_label = ft.Text("Horas", style=self.label_style)
        self.minutes_label = ft.Text("Minutos", style=self.label_style)
        self.seconds_label = ft.Text("Segundos", style=self.label_style)
        
        # Contenedores
        self.hours_box = self._create_box(self.hours_text, self.hours_label)
        self.minutes_box = self._create_box(self.minutes_text, self.minutes_label)
        self.seconds_box = self._create_box(self.seconds_text, self.seconds_label)
        
        # Layout
        self.content = ft.Row(
            [self.hours_box, self.minutes_box, self.seconds_box],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40
        )
        
        # Si hay un start_time previo, mostrar el tiempo actual
        if self.start_time:
            self._update_display()
    
    def _create_box(self, text_control, label_control):
        """Crea un contenedor para cada componente de tiempo."""
        return ft.Container(
            content=ft.Column(
                [text_control, label_control],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            ),
            **self.box_style
        )
    
    def start(self):
        """
        Inicia el cronómetro.
        
        Returns:
            datetime: Momento exacto de inicio
        """
        if not self.is_running:
            # Si no hay start_time previo, crear uno nuevo
            if not self.start_time:
                self.start_time = datetime.now()
            
            self.is_running = True
            self.stop_event.clear()
            self._update_display()
            
            # Iniciar hilo de actualización
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()
        
        return self.start_time
    
    def stop(self):
        """
        Detiene el cronómetro.
        
        Returns:
            float: Tiempo transcurrido en segundos
        """
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(timeout=0.5)
                self.timer_thread = None
        
        return self.get_elapsed_seconds()
    
    def reset(self):
        """Reinicia el cronómetro completamente."""
        self.stop()
        self.start_time = None
        self.hours_text.value = "00"
        self.minutes_text.value = "00"
        self.seconds_text.value = "00"
        if self.page:
            self.page.update()
    
    def get_current_time(self):
        """
        Obtiene el tiempo actual del cronómetro.
        
        Returns:
            datetime: Momento actual para mediciones
        """
        return datetime.now()
    
    def get_elapsed_seconds(self):
        """
        Obtiene el tiempo transcurrido en segundos.
        
        Returns:
            float: Segundos transcurridos desde el inicio
        """
        if not self.start_time:
            return 0.0
        return (datetime.now() - self.start_time).total_seconds()
    
    def get_elapsed_time(self):
        """
        Obtiene el tiempo transcurrido como timedelta.
        
        Returns:
            timedelta: Tiempo transcurrido
        """
        if not self.start_time:
            return timedelta(0)
        return datetime.now() - self.start_time
    
    def get_state(self):
        """
        Obtiene el estado completo del cronómetro.
        
        Returns:
            dict: Estado del cronómetro para guardar
        """
        return {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'is_running': self.is_running,
            'elapsed_seconds': self.get_elapsed_seconds()
        }
    
    def _timer_loop(self):
        """Bucle principal del cronómetro."""
        while not self.stop_event.is_set():
            try:
                self._update_display()
                if self.page and hasattr(self.page, 'update'):
                    self.page.update()
                
                if self.stop_event.wait(0.1):  # Actualizar cada 100ms
                    break
                    
            except Exception:
                break
    
    def _update_display(self):
        """Actualiza la visualización del cronómetro."""
        if not self.start_time:
            return
        
        elapsed = datetime.now() - self.start_time
        total_seconds = int(elapsed.total_seconds())
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Limitar horas a 99 para evitar overflow visual
        hours = min(hours, 99)
        
        # Actualizar textos
        self.hours_text.value = f"{hours:02d}"
        self.minutes_text.value = f"{minutes:02d}"
        self.seconds_text.value = f"{seconds:02d}"
    
    def will_unmount(self):
        """Limpia recursos al desmontar el componente."""
        self.stop()


# Ejemplo de uso para carrera
def main(page: ft.Page):
    page.title = "Cronómetro de Carrera"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # Cronómetro - puede iniciarse con tiempo previo para recuperar estado
    # cronometro = Cronometro()  # Nuevo cronómetro
    # cronometro = Cronometro(start_time=datetime(2024, 1, 1, 12, 0, 0))  # Recuperar estado
    cronometro = Cronometro()
    
    status = ft.Text("Cronómetro listo", size=16, color=ft.Colors.WHITE70)
    
    def start_race(e):
        """Inicia la carrera."""
        start_time = cronometro.start()
        status.value = f"Carrera iniciada: {start_time.strftime('%H:%M:%S')}"
        page.update()
    
    def stop_race(e):
        """Detiene la carrera."""
        elapsed = cronometro.stop()
        status.value = f"Carrera detenida. Tiempo total: {elapsed:.2f}s"
        page.update()
    
    def get_checkpoint(e):
        """Obtiene tiempo de checkpoint."""
        if cronometro.start_time:
            checkpoint_time = cronometro.get_current_time()
            elapsed = cronometro.get_elapsed_seconds()
            status.value = f"Checkpoint: {checkpoint_time.strftime('%H:%M:%S')} (T+{elapsed:.2f}s)"
        else:
            status.value = "Debes iniciar el cronómetro primero"
        page.update()
    
    def reset_race(e):
        """Reinicia el cronómetro."""
        cronometro.reset()
        status.value = "Cronómetro reiniciado"
        page.update()
    
    def get_state_info(e):
        """Muestra información del estado."""
        state = cronometro.get_state()
        status.value = f"Estado: {state}"
        page.update()
    
    # Controles
    controls = ft.Row([
        ft.ElevatedButton("INICIAR", on_click=start_race, 
                         bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
        ft.ElevatedButton("PARAR", on_click=stop_race, 
                         bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
        ft.ElevatedButton("Checkpoint", on_click=get_checkpoint, 
                         bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
        ft.ElevatedButton("Reset", on_click=reset_race, 
                         bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE),
        ft.ElevatedButton("Estado", on_click=get_state_info, 
                         bgcolor=ft.Colors.PURPLE, color=ft.Colors.WHITE),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    
    # Layout
    page.add(
        ft.Column([
            ft.Text("🏁 Cronómetro de Carrera", size=32, weight=ft.FontWeight.BOLD),
            cronometro,
            controls,
            status
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    )

if __name__ == "__main__":
    ft.app(target=main)