import flet as ft
from datetime import datetime, timedelta
import threading
import time

class CountdownTimer(ft.Container):
    def __init__(
        self,
        target_date=None,
        on_finish=None,
        # --- Estilos del widget ---
        days_style=None,
        hours_style=None,
        minutes_style=None,
        seconds_style=None,
        label_style=None,
        box_style=None,
        # --- NUEVO: Parámetros para la responsividad ---
        reference_width=550.0,
        min_scale=0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.transform_alignment = ft.alignment.center
        
        # --- Lógica existente ---
        self.target_date = target_date or (datetime.now() + timedelta(hours=4, minutes=26, seconds=38))
        self.on_finish = on_finish
        
        # --- Estilos ---
        self._days_style = days_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self._hours_style = hours_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self._minutes_style = minutes_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self._seconds_style = seconds_style or ft.TextStyle(size=60, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self._label_style = label_style or ft.TextStyle(size=16, color=ft.Colors.WHITE)
        self._box_style = box_style or {
            "bgcolor": ft.Colors.BLUE_300, "border_radius": 10, "padding": 10,
            "width": 100, "height": 130, "alignment": ft.alignment.center,
        }
        
        # --- Componentes UI ---
        self.days_text = ft.Text("00", style=self._days_style)
        self.hours_text = ft.Text("00", style=self._hours_style)
        self.minutes_text = ft.Text("00", style=self._minutes_style)
        self.seconds_text = ft.Text("00", style=self._seconds_style)
        
        self.days_label = ft.Text("Días", style=self._label_style)
        self.hours_label = ft.Text("Horas", style=self._label_style)
        self.minutes_label = ft.Text("Minutos", style=self._label_style)
        self.seconds_label = ft.Text("Segundos", style=self._label_style)
        
        # --- Contenedores ---
        def create_box(text_control, label_control):
            return ft.Container(
                content=ft.Column(
                    [text_control, label_control],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                ),
                **self._box_style
            )
        
        self.days_box = create_box(self.days_text, self.days_label)
        self.hours_box = create_box(self.hours_text, self.hours_label)
        self.minutes_box = create_box(self.minutes_text, self.minutes_label)
        self.seconds_box = create_box(self.seconds_text, self.seconds_label)
        
        self.content = ft.Row(
            [self.days_box, self.hours_box, self.minutes_box, self.seconds_box],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        )
        
        # --- Lógica de hilos ---
        self.is_running = False
        self.timer_thread = None
        self.stop_event = threading.Event()

        # --- NUEVO: Propiedades para la responsividad ---
        self.reference_width = reference_width
        self.min_scale = min_scale
        # Aseguramos que el control se pueda escalar
        self.scale = 1.0

    # MODIFICADO: did_mount ahora también gestiona la responsividad
    def did_mount(self):
        """Se llama cuando el componente es montado en la UI."""
        self.start()  # Inicia el temporizador
        
        # --- NUEVO: Lógica de responsividad ---
        if self.page:
            self.page.on_resize = self._handle_resize
            self._handle_resize(None) # Llama una vez para ajustar tamaño inicial

    # MODIFICADO: will_unmount ahora limpia el evento on_resize
    def will_unmount(self):
        """Se llama cuando el componente es desmontado de la UI."""
        self.stop()  # Detiene el temporizador
        
        # --- NUEVO: Limpieza del evento ---
        if self.page and self.page.on_resize == self._handle_resize:
            self.page.on_resize = None
    
    # NUEVO: Método interno para manejar el redimensionamiento
    def _handle_resize(self, e):
        """Ajusta la escala del widget basado en el ancho de la página."""
        if not self.page:
            return

        page_width = self.page.width or self.reference_width
        
        new_scale = min(1.0, page_width / self.reference_width)
        self.scale = max(self.min_scale, new_scale)
        
        self.update()

    # --- Resto de los métodos del temporizador (sin cambios) ---
    def _timer_loop(self):
        while not self.stop_event.is_set():
            self._update_time_values()
            if self.page:
                self.page.update()
            time.sleep(1)
    
    def start(self):
        if not self.is_running:
            self.is_running = True
            self.stop_event.clear()
            self._update_time_values()
            self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
            self.timer_thread.start()
    
    def stop(self):
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            if self.timer_thread:
                self.timer_thread.join(timeout=1)
                self.timer_thread = None
    
    def set_target_date(self, new_date):
        self.target_date = new_date
        self._update_time_values()
        if self.page:
            self.page.update()
    
    def _update_time_values(self):
        now = datetime.now()
        if now >= self.target_date:
            time_diff = timedelta(0)
            if self.on_finish and self.is_running:
                # Detener antes de llamar a on_finish
                self.stop()
                self.on_finish()
        else:
            time_diff = self.target_date - now
        
        days = time_diff.days
        seconds = time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        self.days_text.value = str(days)
        self.hours_text.value = f"{hours:02d}"
        self.minutes_text.value = f"{minutes:02d}"
        self.seconds_text.value = f"{seconds:02d}"
    
    def update_countdown(self):
        self._update_time_values()
        self.update()