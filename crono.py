import flet as ft
from datetime import datetime, timedelta
import threading
import time

class Cronometro(ft.Container):
    def __init__(
        self,
        start_time=None,  # Momento de inicio del cronómetro
        on_finish=None,   # Callback opcional (por si quieres límite máximo)
        max_time=None,    # Tiempo máximo opcional (en segundos)
        # --- Estilos del widget ---
        hours_style=None,
        minutes_style=None,
        seconds_style=None,
        # milliseconds_style=None,
        tam_text=100,
        label_style=None,
        box_style=None,
        # --- Parámetros para la responsividad ---
        reference_width=550.0,
        min_scale=0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.transform_alignment = ft.alignment.center
        
        # --- Lógica del cronómetro ---
        self.start_time = start_time or datetime.now()  # Momento de inicio
        self.on_finish = on_finish
        self.max_time = max_time  # Tiempo máximo en segundos (opcional)
        
        # --- Estilos ---
        self._hours_style = hours_style or ft.TextStyle(size=tam_text, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        self._minutes_style = minutes_style or ft.TextStyle(size=tam_text, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        self._seconds_style = seconds_style or ft.TextStyle(size=tam_text, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        # self._milliseconds_style = milliseconds_style or ft.TextStyle(size=tam_text, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE70)
        self._label_style = label_style or ft.TextStyle(size=30, color=ft.Colors.BLACK)
        self._box_style = box_style or {
            "bgcolor": ft.Colors.GREEN_400, "border_radius": 10, "padding": 10,
            "width": 100, "height": 130, "alignment": ft.alignment.center,
        }
        
        # Estilo especial para milisegundos (más pequeño)
        self._ms_box_style = dict(self._box_style)
        self._ms_box_style["width"] = self._box_style["width"] + 40
        
        # --- Componentes UI ---
        self.hours_text = ft.Text("00", style=self._hours_style)
        self.minutes_text = ft.Text("00", style=self._minutes_style)
        self.seconds_text = ft.Text("00", style=self._seconds_style)
        # self.milliseconds_text = ft.Text("000", style=self._milliseconds_style)
        
        self.hours_label = ft.Text("Horas", style=self._label_style)
        self.minutes_label = ft.Text("Minutos", style=self._label_style)
        self.seconds_label = ft.Text("Segundos", style=self._label_style)
        # self.milliseconds_label = ft.Text("Milisegundos", style=self._label_style)
        
        # --- Contenedores ---
        def create_box(text_control, label_control, box_style=None):
            style = box_style or self._box_style
            return ft.Container(
                content=ft.Column(
                    [text_control, label_control],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                ),
                **style
            )
        
        self.hours_box = create_box(self.hours_text, self.hours_label)
        self.minutes_box = create_box(self.minutes_text, self.minutes_label)
        self.seconds_box = create_box(self.seconds_text, self.seconds_label)
        # self.milliseconds_box = create_box(self.milliseconds_text, self.milliseconds_label, self._ms_box_style)
        
        self.content = ft.Row(
            [self.hours_box, self.minutes_box, self.seconds_box],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        # --- Lógica de hilos ---
        self.is_running = False
        self.timer_thread = None
        self.stop_event = threading.Event()

        # --- Propiedades para la responsividad ---
        self.reference_width = reference_width
        self.min_scale = min_scale
        self.scale = 1.0

    def did_mount(self):
        """Se llama cuando el componente es montado en la UI."""
        self.start()  # Inicia el cronómetro
        
        # Lógica de responsividad
        if self.page:
            self.page.on_resize = self._handle_resize
            self._handle_resize(None)

    def will_unmount(self):
        """Se llama cuando el componente es desmontado de la UI."""
        self.cleanup()  # Usa el método de limpieza completo
    
    def _handle_resize(self, e):
        """Ajusta la escala del widget basado en el ancho de la página."""
        if not self.page:
            return

        page_width = self.page.width or self.reference_width
        
        new_scale = min(1.0, page_width / self.reference_width)
        self.scale = max(self.min_scale, new_scale)
        
        self.update()

    def _timer_loop(self):
        """Bucle principal del cronómetro con mayor precisión."""
        while not self.stop_event.is_set():
            try:
                self._update_time_values()
                # Verificar si la página sigue activa antes de actualizar
                if self.page and hasattr(self.page, 'update'):
                    try:
                        self.page.update()
                    except Exception:
                        # Si falla la actualización, detener el hilo
                        break
                
                # Usar wait en lugar de sleep para responder más rápido al stop_event
                if self.stop_event.wait(0.01):  # 10ms timeout
                    break
                    
            except Exception:
                # Si hay cualquier error, salir del bucle
                break
    
    def start(self):
        """Inicia el cronómetro."""
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self._update_time_values()
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()
    
    def stop(self):
        """Detiene el cronómetro."""
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            if self.timer_thread and self.timer_thread.is_alive():
                self.timer_thread.join(timeout=0.5)  # Timeout más corto
                self.timer_thread = None
    
    def reset(self, new_start_time=None):
        """Reinicia el cronómetro con un nuevo tiempo de inicio."""
        was_running = self.is_running
        self.stop()
        
        self.start_time = new_start_time or datetime.now()
        self._update_time_values()
        
        if self.page:
            self.page.update()
        
        if was_running:
            self.start()
    
    def set_start_time(self, new_start_time):
        """Establece un nuevo tiempo de inicio (para recuperación de estado)."""
        self.start_time = new_start_time
        self._update_time_values()
        if self.page:
            self.page.update()
    
    def get_elapsed_time(self):
        """Retorna el tiempo transcurrido como timedelta."""
        return datetime.now() - self.start_time
    
    def get_elapsed_seconds(self):
        """Retorna el tiempo transcurrido en segundos totales."""
        return self.get_elapsed_time().total_seconds()
    
    def _update_time_values(self):
        """Actualiza los valores del cronómetro."""
        # Verificar si el cronómetro sigue activo
        if not self.is_running and self.stop_event.is_set():
            return
            
        now = datetime.now()
        elapsed = now - self.start_time
        
        # Verificar límite máximo si está establecido
        if self.max_time and elapsed.total_seconds() >= self.max_time:
            if self.on_finish and self.is_running:
                self.stop()
                self.on_finish()
            elapsed = timedelta(seconds=self.max_time)
        
        # Calcular componentes de tiempo
        total_seconds = int(elapsed.total_seconds())
        milliseconds = int(elapsed.microseconds / 1000)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        # Limitar horas a 99 para evitar overflow visual
        hours = min(hours, 99)
        
        # Actualizar textos (verificar que los objetos existan)
        if hasattr(self, 'hours_text') and self.hours_text:
            self.hours_text.value = f"{hours:02d}"
        if hasattr(self, 'minutes_text') and self.minutes_text:
            self.minutes_text.value = f"{minutes:02d}"
        if hasattr(self, 'seconds_text') and self.seconds_text:
            self.seconds_text.value = f"{seconds:02d}"
        if hasattr(self, 'milliseconds_text') and self.milliseconds_text:
            self.milliseconds_text.value = f"{milliseconds:03d}"
    
    def cleanup(self):
        """Limpia todos los recursos del cronómetro."""
        self.stop()
        if self.page and hasattr(self.page, 'on_resize') and self.page.on_resize == self._handle_resize:
            self.page.on_resize = None
    
    def update_display(self):
        """Actualiza la visualización manualmente."""
        self._update_time_values()
        self.update()


# Ejemplo de uso y demostración
def main(page: ft.Page):
    page.title = "Cronómetro Progresivo"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.spacing = 20
    
    # Función que se ejecuta cuando alcanza el límite (opcional)
    def on_timer_finish():
        print("¡Cronómetro terminado!")
        # Aquí podrías mostrar una alerta, guardar datos, etc.
    
    # Crear cronómetro
    # Para recuperar estado, pasarías el start_time guardado anteriormente
    cronometro = Cronometro(
        start_time=datetime.now(),  # Para nueva sesión
        # start_time=datetime(2024, 1, 1, 12, 0, 0),  # Para recuperar estado
        max_time=3600,  # Límite de 1 hora (opcional)
        on_finish=on_timer_finish
    )
    
    # Manejar el cierre de la ventana/aplicación
    def on_window_close(e):
        cronometro.cleanup()
    
    page.on_window_event = lambda e: on_window_close(e) if e.data == "close" else None
    
    # Botones de control
    def reset_timer(e):
        cronometro.reset()
        status.value = f"Cronómetro reiniciado: {cronometro.start_time}"
        page.update()
    
    def stop_timer(e):
        cronometro.stop()
        elapsed = cronometro.get_elapsed_seconds()
        status.value = f"Cronómetro detenido. Tiempo: {elapsed:.2f}s"
        page.update()
    
    def start_timer(e):
        cronometro.start()
        status.value = "Cronómetro iniciado"
        page.update()
    
    def get_state(e):
        elapsed = cronometro.get_elapsed_seconds()
        status.value = f"Inicio: {cronometro.start_time} | Transcurrido: {elapsed:.2f}s"
        page.update()
    
    # Controles
    controls = ft.Row([
        ft.ElevatedButton("Iniciar", on_click=start_timer, color=ft.Colors.GREEN),
        ft.ElevatedButton("Detener", on_click=stop_timer, color=ft.Colors.RED),
        ft.ElevatedButton("Reiniciar", on_click=reset_timer, color=ft.Colors.BLUE),
        ft.ElevatedButton("Ver Estado", on_click=get_state, color=ft.Colors.ORANGE),
    ], alignment=ft.MainAxisAlignment.CENTER)
    
    status = ft.Text(
        f"Cronómetro iniciado: {datetime.now()}",
        size=14,
        color=ft.Colors.WHITE70
    )
    
    # Layout principal
    page.add(
        ft.Column([
            ft.Text("Cronómetro Progresivo", size=30, weight=ft.FontWeight.BOLD),
            cronometro,
            controls,
            status
        ], alignment=ft.MainAxisAlignment.CENTER, 
           horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)