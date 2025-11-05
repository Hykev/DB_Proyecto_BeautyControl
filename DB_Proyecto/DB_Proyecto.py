"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

from .db import seed_cities  # <-- importar la función nueva


class State(rx.State):
    """The app state."""

    status_message: str = ""  # mensaje para mostrar el resultado


    def crear_cities(self):
        """Acción del botón: llenar Countries y Cities si están vacías."""
        ok = seed_cities()
        if ok:
            self.status_message = "✅ Datos de Countries y Cities creados correctamente."
        else:
            self.status_message = "❌ Hubo un error al crear los datos. Revisa la consola."


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.heading("Hola!", size="7"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),

            # 🔽 NUEVO BOTÓN para crear datos en Cities
            rx.button(
                "Crear datos de Cities",
                on_click=State.crear_cities,
                size="3",
            ),

            # Mensaje de estado después de presionar el botón
            rx.cond(
                State.status_message != "",
                rx.text(State.status_message, size="4"),
            ),

            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
