import flet as ft
import threading
from utils.crono import Cronometro
from datetime import datetime, timedelta
from camara import Camara  

imagenes_patrocinadores = [
    ("assets/banner_pitma.png","https://pitma.es/"),
    ("assets/banner_artipublic.png","https://www.artipubli.com/"),
    ("assets/banner_andros.png","https://androsvegetal.es/"),
    ("assets/banner_bathco.png","https://www.thebathcollection.com/"),
    ("assets/banner_lavin.png","https://www.almaceneslavin.com/"),
    ("assets/banner_natuber.png","https://natuber.com/"),
    ("assets/banner_rionansa.png","https://aytorionansa.com/"),
    ("assets/banner_jvcosio.png","https://juntavecinalcosiorozadio.blogspot.com/"),
    ("assets/banner_aljomar.png","https://www.aljomar.es/"),
    ("assets/banner_grupochovi.png","https://www.chovi.com/es/"),
    ("assets/banner_LIS.png","https://www.lisdatasolutions.com/es/"),
    ("assets/banner_carandia.png","https://carandiadistribuciones.com/"),
]



class DashboardApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = "#333333"
        
        self.camara = Camara(width=float("inf"), height=float("inf"))  # Ajustar el ancho y alto de la cámara
        
        # Definir atributos del atleta ANTES de construir la UI
        self.nombreAtleta = "David"
        self.apellidoAtleta = "GONZALEZ RUIZ"
        self.CategoriaAtleta = "Senior"
        self.tiempoAtleta = timedelta(hours=0, minutes=0, seconds=0)  # Tiempo inicial del atleta
        
        self.setup_page()
        self.build_ui()
    
    def setup_page(self):
        """Configuración inicial de la página"""
        self.page.title = "Dashboard App"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.spacing = 20
        self.page.window.width = 1200
        self.page.window.height = 800
        
        self.cronometro = Cronometro()
        
        self.btn_start = ft.ElevatedButton(
            "INICIAR",
            on_click=lambda e: self.iniciar_cronometro(),
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            width=200,
            height=100,
            icon=ft.Icons.PLAY_ARROW,
        )
        self.estado_camara = False
        # Crear un switch para activar/desactivar la cámara
        self.sw_camara = ft.Switch(
            value=self.estado_camara,
            label="Iniciar camara con visión artificial",
            on_change=lambda e: self.iniciar_camara(),
        )
        
        # self.btn_start = ft.IconButton(
        #     icon=ft.Icons.PLAY_ARROW,
        #     icon_size=100,
        #     tooltip="Iniciar Cronómetro",
        #     on_click=lambda e: self.cronometro.start(),
        #     icon_color=ft.Colors.GREEN_700,
        # )
        
    def create_container(self, content, color: str, width: int = None, height: int = None, expand: bool = True):
        """Crea un contenedor con texto centrado"""
        # Si el contenido es una cadena, convertirla a ft.Text
        if isinstance(content, str):
            content = ft.Text(
                content,
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER
            )
        
        return ft.Container(
                content=content,
                width=width,
                height=height,
                bgcolor=color,
                border_radius=20,
                alignment=ft.alignment.center,
                padding=20,
                expand=expand,
            )
    
    def create_complex_container(self):
        """Crea el contenedor complejo con subcontenedores"""
        return ft.Container(
            bgcolor=ft.Colors.BLUE_700,
            border_radius=10,
            alignment=ft.alignment.center,
            padding=10,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            [                               
                                self.create_container("", color= ft.Colors.BLUE_ACCENT, width=250, expand=False),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Text(f"{self.nombreAtleta} {self.apellidoAtleta}", size=40, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                                            ft.Text(f"{self.tiempoAtleta}", size=60, color=ft.Colors.WHITE)                                    
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=10,
                                    expand=True,
                                    bgcolor=ft.Colors.BLUE_ACCENT,
                                    border_radius=10,
                                ),
                            ],
                            # alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor=ft.Colors.YELLOW_300,  # Added background color
                        border_radius=10,
                        alignment=ft.alignment.center,
                        padding=10,
                        height=180,
                    ),
                                        
                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[0][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[1][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[2][0], width=270, height=170),    
                            ft.Image(src=imagenes_patrocinadores[3][0], width=270, height=170),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[4][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[5][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[6][0], width=270, height=170),   
                            ft.Image(src=imagenes_patrocinadores[7][0], width=270, height=170), 
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[8][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[9][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[10][0], width=270, height=170),   
                            ft.Image(src=imagenes_patrocinadores[11][0], width=270, height=170), 
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[11][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[11][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[11][0], width=270, height=170),    
                            ft.Image(src=imagenes_patrocinadores[11][0], width=270, height=170),    
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                
                
                ],
                spacing=20
            )
            
        )
    
    def build_ui(self):
        """Construye la interfaz de usuario"""
        
        # Fila superior
        top_row = ft.Row(
            controls=[
                # Logo
                ft.Container(
                    content=ft.Image(
                        src="assets/logo.png",
                        expand=True,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    width=1100,
                    height=330,
                    border_radius=ft.border_radius.all(20),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    bgcolor=ft.Colors.RED_700,
                ),
                
                # Cronómetro
                self.create_container(
                    content = self.cronometro,
                    color = ft.Colors.TRANSPARENT, 
                    width=200,
                    height=400, expand=True
                ),
                # Botón de inicio del cronómetro
                self.btn_start,
                
            ],
            spacing=5,
            expand=False,
        )
        
        # Fila inferior       
        inf_fila = ft.Row(
            controls=[
                # Contenedor de la izquierda
                
                self.create_container(
                    content = ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text("🏁 IA META 2.0", size=50, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            self.sw_camara,
                            # Mostrar el contenedor de la cámara solo si está activa
                            self.create_container(
                                self.camara.video_container, 
                                color=ft.Colors.GREEN_700, 
                                expand=True
                            ) if self.estado_camara else ft.Container(
                                content=ft.Text(
                                    "Cámara desactivada",
                                    size=20,
                                    color=ft.Colors.WHITE54,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                expand=True,
                                alignment=ft.alignment.center
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                      
                    color = ft.Colors.GREEN_700, 
                    expand=True
                ),
                self.create_complex_container()
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            expand=True,
        )

        main_layout = ft.Column(
            controls=[
                top_row,
                inf_fila
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            spacing=10,
        )
        
        # Agregar a la página
        self.page.add(main_layout)
        self.page.update()

    def rebuild_ui(self):
        """Reconstruye la interfaz de usuario"""
        # Limpiar la página
        self.page.controls.clear()
        
        # Reconstruir la interfaz
        self.build_ui()
    
    def iniciar_camara(self):
        """Inicia/detiene la cámara en un hilo separado"""
        if not self.estado_camara:
            print("Iniciando cámara...")
            threading.Thread(target=self.camara.capture_video, args=(self.page,), daemon=True).start()
            self.estado_camara = True
        else:
            print("Deteniendo cámara...")
            self.estado_camara = False
        
        # Reconstruir la interfaz para mostrar/ocultar la cámara
        self.rebuild_ui()
        self.page.update()
        
    def iniciar_cronometro(self):
        """Inicia el cronómetro"""
        # self.btn_start.disabled = True
        # self.btn_start.visible = False
        self.btn_start.text = "Refrescar"
        tiempo_inicio = self.cronometro.start()
        print(f"Cronómetro iniciado a las: {tiempo_inicio}")
        self.page.update()

def main(page: ft.Page):
    """Función principal de la aplicación"""
    app = DashboardApp(page)
    # Iniciar la cámara automáticamente en un hilo
    # import threading
    # threading.Thread(target=app.camara.capture_video, args=(page,), daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)