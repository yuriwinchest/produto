import flet as ft
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import os
import signal
import base64

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, page):
        self.page = page

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print("File changed, reloading...")
            os.kill(os.getpid(), signal.SIGINT)

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLACK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    page.main_image_src = "img/123.png"
    page.default_image_src = page.main_image_src
    page.smaller_images = ["img/cadeira2.webp", "img/cadeirafrente.webp", "img/cadeirapesssoa.webp"]
    page.color_options = {
        "Amarelo": "img/123.png",
        "Verde": "img/green_chair.png",
        "Cinza": "img/gray_chair.png"
    }
    build_layout(page)

def is_accessible(path):
    if os.path.isfile(path):
        print(f"Arquivo encontrado: {path}")
        return True
    else:
        print(f"Arquivo não encontrado: {path}")
        return False

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def update_main_image(page, image_src):
    main_image_base64 = image_to_base64(image_src)
    main_image_src = f"data:image/png;base64,{main_image_base64}"
    page.main_image.src = main_image_src
    page.update()

def build_layout(page):
    def create_hoverable_image(src):
        if not is_accessible(src):
            print(f"Imagem não acessível: {src}")
            return ft.Container(width=80, height=80)

        image_base64 = image_to_base64(src)
        image_src = f"data:image/png;base64,{image_base64}"

        def on_hover(e):
            if e.data == "true":
                update_main_image(page, src)
            else:
                update_main_image(page, page.default_image_src)

        return ft.GestureDetector(
            content=ft.Image(
                src=image_src,
                width=80,
                height=80,
                fit=ft.ImageFit.CONTAIN,
            ),
            on_hover=on_hover,
        )

    thumbnails = [create_hoverable_image(src) for src in page.smaller_images]

    main_image_base64 = image_to_base64(page.main_image_src)
    main_image_src = f"data:image/png;base64,{main_image_base64}"

    page.main_image = ft.Image(
        src=main_image_src,
        width=350,
        height=350,
        fit=ft.ImageFit.CONTAIN
    )

    product_images = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=page.main_image,
                    border=ft.border.all(2, ft.colors.YELLOW),
                    padding=5,
                ),
                ft.Row(
                    controls=thumbnails,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        bgcolor=ft.colors.WHITE,  # Fundo branco para a seção de imagens
        padding=10,
        border_radius=10
    )

    def on_color_change(e):
        color = e.control.value
        new_image_src = page.color_options.get(color, page.main_image_src)
        page.default_image_src = new_image_src  # Atualiza a imagem padrão para a cor selecionada
        update_main_image(page, new_image_src)

    product_details = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("CADEIRAS", size=14, color=ft.colors.YELLOW),
                ft.Text("Poltrona Amarela Moderna", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("R$ 399", size=20, color=ft.colors.YELLOW),
                ft.Row(
                    controls=[ft.Icon(name="star", color=ft.colors.YELLOW) for _ in range(5)],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Divider(color=ft.colors.WHITE24),
                ft.Text("Descrição", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Dimensões: 85cm de largura, 80cm de altura e 75cm de profundidade", size=12, color=ft.colors.WHITE60),
                ft.Text("Material: 100% poliéster, Estrutura: Madeira de eucalipto", size=12, color=ft.colors.WHITE60),
                ft.Divider(color=ft.colors.WHITE24),
                ft.Row(
                    controls=[
                        ft.Dropdown(
                            label="Cor",
                            options=[
                                ft.dropdown.Option("Amarelo"),
                                ft.dropdown.Option("Verde"),
                                ft.dropdown.Option("Cinza"),
                            ],
                            width=200,
                            on_change=on_color_change,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.TRANSPARENT,
                            border_color=ft.colors.WHITE24,
                        ),
                        ft.Dropdown(
                            label="Quantidade",
                            options=[
                                ft.dropdown.Option("1 unid."),
                                ft.dropdown.Option("2 unid."),
                                ft.dropdown.Option("3 unid."),
                            ],
                            width=200,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.TRANSPARENT,
                            border_color=ft.colors.WHITE24,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            "Adicionar à lista de desejos",
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.TEAL_700,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            width=350,
                        ),
                        ft.ElevatedButton(
                            "Adicionar ao carrinho",
                            style=ft.ButtonStyle(
                                color=ft.colors.BLACK,
                                bgcolor=ft.colors.YELLOW,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            width=350,
                        )
                    ],
                    spacing=10,
                ),
            ],
            spacing=20,
        ),
        bgcolor=ft.colors.BLACK,  # Fundo preto para a seção de detalhes
        padding=20,
        border=ft.border.all(1, ft.colors.YELLOW),
        border_radius=10
    )

    layout = ft.Container(
        width=1000,
        height=600,
        padding=ft.padding.all(20),
        bgcolor=ft.colors.BLACK,
        border=ft.border.all(2, ft.colors.YELLOW),  # Borda amarela em torno de todo o layout
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.CYAN),  # Efeito de sombra
        content=ft.Row(
            controls=[
                ft.Container(
                    content=product_images,
                    width=400,
                    bgcolor=ft.colors.WHITE,
                    border_radius=10,
                    padding=10
                ),
                ft.Container(
                    width=40,
                ),
                ft.Container(
                    content=product_details,
                    width=500,
                    bgcolor=ft.colors.BLACK,
                    border_radius=10,
                    padding=10
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    page.clean()
    page.add(
        ft.Container(
            content=layout,
            alignment=ft.alignment.center  # Centraliza o layout
        )
    )
    page.update()

if __name__ == '__main__':
    observer = Observer()
    event_handler = ReloadHandler(None)
    observer.schedule(event_handler, path='.', recursive=True)
    observer_thread = threading.Thread(target=observer.start)
    observer_thread.start()

    try:
        ft.app(target=main, view=ft.WEB_BROWSER)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        observer.stop()
        observer_thread.join()
        observer.join()
