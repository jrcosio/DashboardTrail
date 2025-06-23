import flet as ft

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
        
    def create_container(self, text: str, color: str, width: int = None, height: int = None, expand: bool = True):
        """Crea un contenedor con texto centrado"""
        return ft.Container(
            content=ft.Text(
                text,
                size=16,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE if color in [ft.Colors.RED_700, ft.Colors.GREEN_700] else ft.Colors.BLACK,
                text_align=ft.TextAlign.CENTER
            ),
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
                                    weight=60,
                                    height=50,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                    bgcolor=ft.Colors.BLUE_300,
                                    
                                ),
                                ft.Text(
                                    "Datos de Dorsal",
                                    size=20,
                                    weight=1200,
                                    height=50,
                                    color=ft.Colors.WHITE,
                                    bgcolor=ft.Colors.RED,
                                    
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        # bgcolor=ft.Colors.BLUE_300,
                        # border_radius=10,
                        # height=100,
                        alignment=ft.alignment.center,
                        padding=10,
                        expand=True,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Subcontenedor 3",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor=ft.Colors.BLUE_200,
                        border_radius=10,
                        height=400,
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
                    "Cronometro", 
                    ft.Colors.RED_700, 
                    height=150,
                )
            ],
            spacing=10,
            expand=True
        )
        
        # Fila inferior       
        inf_fila = ft.Row(
            controls=[
                # Contenedor de la izquierda
                self.create_container(
                    "Contenedor Izquierdo", 
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