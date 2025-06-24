import flet as ft
from crono import Cronometro
from datetime import datetime, timedelta

class DashboardApp:
    def __init__(self, page: ft.Page):
        self.page = page
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
                                ft.Text(
                                    "Dorsal",
                                    size=20,
                                    weight=ft.FontWeight.W_600,  # Fixed: use proper FontWeight enum
                                    height=50,
                                    color=ft.Colors.BLACK,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "Datos de Dorsal",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,  # Fixed: use proper FontWeight enum
                                    height=50,
                                    color=ft.Colors.BLACK,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        bgcolor=ft.Colors.YELLOW_300,  # Added background color
                        border_radius=10,
                        alignment=ft.alignment.center,
                        padding=10,
                        height=100,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Patrocinadores",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor=ft.Colors.BLUE_200,
                        border_radius=10,
                        height=370,
                        alignment=ft.alignment.center,
                        padding=10,
                        expand=True,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
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
                                "bgcolor": ft.Colors.RED_400, "border_radius": 10, "padding": 5,
                                "width": 200, "height": 180, "alignment": ft.alignment.center,
                        },
                        tam_text=100,
                        # start_time=datetime(2024, 1, 1, 12, 0, 0),  # Para recuperar estado
                ), 
                    ft.Colors.TRANSPARENT, 
                    width=200,
                    height=180
                )
            ],
            spacing=5,
            expand=False
        )
        
        # Fila inferior       
        inf_fila = ft.Row(
            controls=[
                # Contenedor de la izquierda
                self.create_container(
                    "Imagenes camara", 
                    ft.Colors.GREEN_700, 
                    width=450, 
                    height=500,
                    expand=True
                ),
                # Contenedor del medio (complejo)
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
            spacing=10,
        )
        
        # Agregar a la página
        self.page.add(main_layout)
        self.page.update()

def main(page: ft.Page):
    """Función principal de la aplicación"""
    app = DashboardApp(page)

if __name__ == "__main__":
    ft.app(target=main)