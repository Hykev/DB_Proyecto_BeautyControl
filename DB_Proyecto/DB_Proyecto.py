import reflex as rx
from rxconfig import config
from .pages.customers_page import customers_page
from .pages.products_page import products_page
from .pages.orders_page import orders_page
from .pages.inventory_page import inventory_page
from .pages.promos_loyalty_page import promos_loyalty_page


# Si luego quieres usar la BD desde aquí:
# from . import db


# =========================
# Estado global
# =========================

class State(rx.State):
    """Estado global de la app LootBox."""

    # --- Autenticación ---
    logged_in: bool = False
    username: str = ""
    password: str = ""
    login_error: str = ""

    # --- Navegación interna del dashboard ---
    current_section: str = "resumen"  # resumen | customers | products | orders | inventory | promos | analytics | admin

    # Mensajes generales (para mostrar info/errores arriba)
    global_message: str = ""

    # ---------- LÓGICA DE LOGIN ----------

    def do_login(self):
        """Login mínimo: usuario / contraseña fijos por ahora."""
        # Más adelante podemos validar contra la tabla Users.
        if self.username == "admin" and self.password == "admin":
            self.logged_in = True
            self.login_error = ""
            self.global_message = "Bienvenido a LootBox, admin."
            self.current_section = "resumen"
        else:
            self.login_error = "Usuario o contraseña incorrectos."

    def logout(self):
        """Cerrar sesión."""
        self.logged_in = False
        self.username = ""
        self.password = ""
        self.current_section = "resumen"
        self.global_message = ""

    # ---------- NAVEGACIÓN EN EL DASHBOARD ----------

    def go_to(self, section: str):
        """Cambiar de sección en el dashboard."""
        self.current_section = section


# =========================
# Componentes de UI base
# =========================

def lootbox_logo() -> rx.Component:
    """Logo simple de LootBox."""
    return rx.hstack(
        rx.box(
            "LB",
            bg="orange.9",
            color="white",
            font_weight="bold",
            padding="0.35rem 0.6rem",
            border_radius="999px",
            font_size="0.9rem",
        ),
        rx.text(
            "LootBox",
            font_weight="bold",
            font_size="1.2rem",
            color="orange.9",
        ),
        spacing="2",
        align="center",
    )


def shell(content: rx.Component) -> rx.Component:
    """
    Layout general para páginas internas:
    - Barra superior con logo y botón de logout.
    - Fondo gris claro y contenido centrado.
    """
    return rx.box(
        # Barra superior
        rx.hstack(
            lootbox_logo(),
            rx.spacer(),
            rx.text("Panel de administración", color="gray.9"),
            rx.button(
                "Cerrar sesión",
                variant="soft",
                color_scheme="orange",
                size="2",
                on_click=State.logout,
            ),
            padding_x="1.5rem",
            padding_y="0.75rem",
            border_bottom="1px solid #e2e2e2",
            bg="white",
            align_items="center",
        ),
        # Contenido
        rx.box(
            rx.center(
                content,
                padding="1.5rem",
            ),
            bg="#f7f4f0",  # gris cálido que combina con naranja
            min_height="calc(100vh - 3rem)",
        ),
    )


# =========================
# Secciones del dashboard (contenido principal)
# =========================

def resumen_section() -> rx.Component:
    """Sección de resumen inicial (KPI dummy por ahora)."""
    return rx.vstack(
        rx.heading("Resumen general", size="6", color="orange.9"),
        rx.text(
            "Bienvenido al panel de LootBox. Aquí verás un resumen de clientes, productos, órdenes e inventario.",
            color="gray.9",
        ),
        rx.hstack(
            _kpi_card("Clientes", "500+", "Coleccionistas registrados"),
            _kpi_card("Productos", "2,000+", "Figuras, funkos y más"),
            _kpi_card("Órdenes", "5,000+", "Historial de compras"),
            _kpi_card("Devoluciones", "600", "Gestión de returns"),
            spacing="4",
            wrap="wrap",
        ),
        spacing="4",
        width="100%",
    )


def _kpi_card(title: str, value: str, subtitle: str) -> rx.Component:
    """Card simple para mostrar KPIs en el dashboard."""
    return rx.box(
        rx.vstack(
            rx.text(title, font_weight="medium", color="gray.10"),
            rx.heading(value, size="6", color="orange.9"),
            rx.text(subtitle, font_size="0.8rem", color="gray.8"),
            spacing="1",
        ),
        bg="white",
        padding="1rem 1.25rem",
        border_radius="1rem",
        box_shadow="0 8px 16px rgba(15, 23, 42, 0.08)",
        min_width="13rem",
    )


def placeholder_section(title: str, description: str) -> rx.Component:
    """
    Sección temporal para cada módulo hasta que conectemos con la BD.
    Luego aquí vamos a meter tablas, formularios, etc.
    """
    return rx.vstack(
        rx.heading(title, size="6", color="orange.9"),
        rx.text(description, color="gray.9"),
        rx.box(
            rx.text(
                "✨ Próximamente: aquí irán tablas, filtros, paginación y CRUD "
                "conectado a la base de datos LootBox.",
                color="gray.8",
            ),
            bg="#fff8f0",
            border_radius="1rem",
            padding="1rem",
            border="1px dashed #f97316",
        ),
        spacing="4",
        width="100%",
    )

def dashboard_content() -> rx.Component:
    """Selecciona qué sección mostrar según State.current_section."""
    return rx.cond(
        State.current_section == "resumen",
        resumen_section(),
        rx.cond(
            State.current_section == "customers",
            customers_page(),
            rx.cond(
                State.current_section == "products",
                products_page(),
                rx.cond(
                    State.current_section == "orders",
                    orders_page(),
                    rx.cond(
                        State.current_section == "inventory",
                        inventory_page(),
                        rx.cond(
                            State.current_section == "promos",
                            promos_loyalty_page(),  # <--- aquí usamos la vista real
                            rx.cond(
                                State.current_section == "analytics",
                                placeholder_section(
                                    "Analítica",
                                    "Vistas avanzadas, KPIs y EXPLAIN de consultas.",
                                ),
                                placeholder_section(
                                    "Administración & Auditoría",
                                    "Registros de auditoría y configuración del sistema.",
                                ),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )



# =========================
# Sidebar de navegación del dashboard
# =========================

def sidebar() -> rx.Component:
    """Sidebar con las secciones principales de LootBox."""
    def nav_button(label: str, section: str, icon: str = "•") -> rx.Component:
        return rx.button(
            rx.hstack(
                rx.text(icon, font_weight="bold"),
                rx.text(label),
                spacing="2",
            ),
            justify="flex-start",
            width="100%",
            variant=rx.cond(
                State.current_section == section,
                "solid",
                "ghost",
            ),
            color_scheme="orange",
            on_click=lambda: State.go_to(section),
        )

    return rx.box(
        rx.vstack(
            lootbox_logo(),
            rx.text(
                "Panel LootBox",
                font_size="0.85rem",
                color="gray.8",
            ),
            rx.divider(margin_y="0.5rem"),
            nav_button("Resumen", "resumen", "🏠"),
            nav_button("Clientes", "customers", "👤"),
            nav_button("Productos", "products", "🧸"),
            nav_button("Órdenes", "orders", "🧾"),
            nav_button("Inventario & Logística", "inventory", "📦"),
            nav_button("Promos & Lealtad", "promos", "🎁"),
            nav_button("Analítica", "analytics", "📊"),
            nav_button("Admin & Auditoría", "admin", "🛠️"),
            spacing="1",
            align_items="stretch",
        ),
        width="16rem",
        min_height="60vh",
        bg="white",
        padding="1rem",
        border_radius="1.25rem",
        box_shadow="0 10px 30px rgba(15, 23, 42, 0.08)",
    )


def dashboard_page() -> rx.Component:
    """Estructura completa del dashboard."""
    return shell(
        rx.hstack(
            sidebar(),
            rx.box(
                # Mensaje global (si lo usamos)
                rx.cond(
                    State.global_message != "",
                    rx.box(
                        rx.text(State.global_message, color="orange.10"),
                        bg="#fff7ed",
                        border_radius="0.75rem",
                        padding="0.75rem 1rem",
                        margin_bottom="1rem",
                        border="1px solid #fed7aa",
                    ),
                ),
                dashboard_content(),
                padding="1.25rem 1.5rem",
                bg="white",
                border_radius="1.5rem",
                box_shadow="0 12px 40px rgba(15, 23, 42, 0.08)",
                width="100%",
            ),
            spacing="3",
            align_items="flex-start",
        )
    )


# =========================
# Login Page
# =========================

def login_page() -> rx.Component:
    """Página de Login con estilo acorde a LootBox (naranja + gris claro)."""
    return rx.box(
        rx.center(
            rx.hstack(
                # Lado izquierdo: branding
                rx.box(
                    rx.vstack(
                        lootbox_logo(),
                        rx.heading(
                            "Bienvenido a LootBox",
                            size="7",
                            color="orange.9",
                        ),
                        rx.text(
                            "Panel interno para gestionar clientes, productos, "
                            "órdenes e inventario de coleccionables.",
                            color="gray.9",
                        ),
                        rx.text(
                            "Inicia sesión con tu usuario de administrador para continuar.",
                            font_size="0.9rem",
                            color="gray.8",
                        ),
                        spacing="3",
                    ),
                    max_width="22rem",
                    padding="1.5rem",
                ),
                # Lado derecho: formulario
                rx.box(
                    rx.vstack(
                        rx.heading("Iniciar sesión", size="6", color="gray.10"),
                        rx.input(
                            placeholder="Usuario",
                            value=State.username,
                            on_change=State.set_username,
                        ),
                        rx.input(
                            placeholder="Contraseña",
                            type="password",
                            value=State.password,
                            on_change=State.set_password,
                        ),
                        rx.button(
                            "Entrar",
                            width="100%",
                            color_scheme="orange",
                            size="3",
                            on_click=State.do_login,
                        ),
                        rx.cond(
                            State.login_error != "",
                            rx.text(
                                State.login_error,
                                color="red",
                                font_size="0.85rem",
                            ),
                        ),
                        rx.text(
                            "Tip: por ahora, usuario: admin / contraseña: admin",
                            font_size="0.75rem",
                            color="gray.8",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    bg="white",
                    padding="2rem",
                    border_radius="1.5rem",
                    box_shadow="0 16px 40px rgba(15, 23, 42, 0.12)",
                    width="22rem",
                ),
                spacing="6",
                wrap="wrap",
                justify="center",
            ),
        ),
        bg="#f7f4f0",
        min_height="100vh",
        padding="2rem",
    )


# =========================
# Root page (decide login vs dashboard)
# =========================

def index() -> rx.Component:
    """Página raíz: muestra login o dashboard según el estado."""
    return rx.cond(
        State.logged_in,
        dashboard_page(),
        login_page(),
    )


# =========================
# App de Reflex
# =========================

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="orange",
        radius="large",
        has_background=True,
        panel_background="solid",   
        text_color="gray.12",      
    ),
)

# Página principal
app.add_page(
    index,
    route="/",
    title="LootBox - Panel",
)

