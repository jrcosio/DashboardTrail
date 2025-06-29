import flet as ft
from crono import Cronometro
from datetime import datetime, timedelta
from camara import Camara  # Asegúrate de que el módulo camara.py esté en el mismo directorio   

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
    ("assets/banner_carandia.png","https://carandiadistribuciones.com/L"),
]



class DashboardApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = "#333333"
  
        # self.camara = Camara(width=700, height=700)  
        
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
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),

                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[3][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[4][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[5][0], width=270, height=170),    
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[6][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[7][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[8][0], width=270, height=170),    
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            ft.Image(src=imagenes_patrocinadores[9][0], width=270, height=170),
                            ft.Image(src=imagenes_patrocinadores[10][0], width=270, height=170),
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
                self.create_container(
                    "LOGO", 
                    ft.Colors.RED_700, 
                    width=300, 
                    height=150,
                    expand=False
                ),
                # Cronómetro
               self.create_container(
                    Cronometro(
                        start_time=datetime.now(),  # Para nueva sesión
                        box_style= {
                                "bgcolor": ft.Colors.BLUE_300, "border_radius": 10, "padding": 5,
                                "width": 300, "height": 300, "alignment": ft.alignment.center,
                        },
                        tam_text=180,
                        # start_time=datetime(2024, 1, 1, 12, 0, 0),  # Para recuperar estado
                ), 
                    ft.Colors.TRANSPARENT, 
                    width=200,
                    height=400
                )
            ],
            spacing=5,
            expand=False
        )
        
        # Fila inferior       
        inf_fila = ft.Row(
            controls=[
                # Contenedor de la izquierda
                # self.camara.video_container,
                self.create_container(
                    "Cámara", 
                    ft.Colors.GREEN_700, 
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

def main(page: ft.Page):
    """Función principal de la aplicación"""
    app = DashboardApp(page)
    # Iniciar la cámara automáticamente en un hilo
    import threading
    # threading.Thread(target=app.camara.capture_video, args=(page,), daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)