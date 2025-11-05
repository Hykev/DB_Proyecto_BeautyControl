import reflex as rx
from .. import db


# ===============================
# STATE: Customers
# ===============================

class CustomersState(rx.State):
    """Estado para manejar el CRUD de clientes."""

    # --- Datos y paginación ---
    customers: list[dict] = []
    page: int = 0
    page_size: int = 10
    total_customers: int = 0

    # --- Filtros ---
    search_name: str = ""
    search_email: str = ""

    # --- Formulario (crear / editar) ---
    selected_id: int | None = None
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    telefono: str = ""
    direccion: str = ""
    city_id: int = 1  # valor por defecto

    # --- Mensajes ---
    form_message: str = ""

    # ==========================================================
    # Acciones principales
    # ==========================================================

    def load_customers(self):
        """Carga los clientes con filtros y paginación."""
        self.customers = db.get_customers(
            nombre=self.search_name,
            email=self.search_email,
            page=self.page,
            page_size=self.page_size,
        )

    def next_page(self):
        """Paginación siguiente."""
        self.page += 1
        self.load_customers()

    def prev_page(self):
        """Paginación anterior."""
        if self.page > 0:
            self.page -= 1
        self.load_customers()

    def clear_filters(self):
        """Reinicia filtros y recarga."""
        self.search_name = ""
        self.search_email = ""
        self.page = 0
        self.load_customers()

    # ==========================================================
    # Formulario (crear / editar / eliminar)
    # ==========================================================

    def fill_form(self, customer_id: int):
        """Rellena el formulario con los datos del cliente seleccionado."""
        cliente = db.get_customer_by_id(customer_id)
        if cliente:
            self.selected_id = cliente["ID"]
            self.nombre = cliente["Nombre"]
            self.apellido = cliente["Apellido"]
            self.email = cliente["Email"] or ""
            self.telefono = cliente["Telefono"]
            self.direccion = cliente["Direccion"]
            self.city_id = cliente["Cities_ID"]
            self.form_message = f"Editando cliente #{self.selected_id}"

    def clear_form(self):
        """Limpia el formulario."""
        self.selected_id = None
        self.nombre = ""
        self.apellido = ""
        self.email = ""
        self.telefono = ""
        self.direccion = ""
        self.city_id = 1
        self.form_message = ""

    def save_customer(self):
        """Crea o actualiza un cliente."""
        if not self.nombre or not self.apellido or not self.telefono:
            self.form_message = "Nombre, apellido y teléfono son obligatorios."
            return

        if self.selected_id:
            ok = db.update_customer(
                self.selected_id,
                self.nombre,
                self.apellido,
                self.email,
                self.telefono,
                self.direccion,
                self.city_id,
            )
            self.form_message = (
                "Cliente actualizado correctamente." if ok else "Error al actualizar."
            )
        else:
            ok = db.create_customer(
                self.nombre,
                self.apellido,
                self.email,
                self.telefono,
                self.direccion,
                self.city_id,
            )
            self.form_message = (
                "Cliente creado correctamente." if ok else "Error al crear cliente."
            )

        self.clear_form()
        self.load_customers()

    def delete_customer(self, customer_id: int):
        """Elimina un cliente."""
        ok = db.delete_customer(customer_id)
        self.form_message = (
            "Cliente eliminado correctamente." if ok else "Error al eliminar cliente."
        )
        self.load_customers()


# ===============================
# COMPONENTES DE UI
# ===============================

def customers_table() -> rx.Component:
    """Tabla principal de clientes."""
    headers = [
        "ID",
        "Nombre",
        "Apellido",
        "Email",
        "Teléfono",
        "Ciudad",
        "País",
        "Acciones",
    ]

    def render_row(c: dict):
        """Renderiza una fila de la tabla de clientes (Reflex 0.8+ compatible)."""
        return rx.table.row(
            rx.table.cell(str(c["ID"])),
            rx.table.cell(c["Nombre"]),
            rx.table.cell(c["Apellido"]),
            rx.table.cell(
                rx.cond(
                    c["Email"] != None,
                    c["Email"],
                    "-",
                )
            ),
            rx.table.cell(c["Telefono"]),
            rx.table.cell(
                rx.cond(
                    c.get("Ciudad") != None,
                    c.get("Ciudad"),
                    "",
                )
            ),
            rx.table.cell(
                rx.cond(
                    c.get("Pais") != None,
                    c.get("Pais"),
                    "",
                )
            ),
            rx.table.cell(
                rx.hstack(
                    rx.button(
                        "✏️",
                        size="1",
                        variant="soft",
                        color_scheme="orange",
                        on_click=lambda: CustomersState.fill_form(c["ID"]),
                    ),
                    rx.button(
                        "🗑️",
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        on_click=lambda: CustomersState.delete_customer(c["ID"]),
                    ),
                    spacing="2",
                )
            ),
        )



    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    *[rx.table.column_header_cell(h) for h in headers],
                )
            ),
            rx.table.body(
                rx.foreach(CustomersState.customers, render_row)
            ),
        ),
        width="100%",
        overflow_x="auto",
        bg="white",
        padding="1rem",
        border_radius="1rem",
        box_shadow="0 8px 16px rgba(15,23,42,0.08)",
    )


def customer_form() -> rx.Component:
    """Formulario para crear o editar un cliente."""
    return rx.box(
        rx.vstack(
            rx.heading("Formulario de Cliente", size="5", color="orange.9"),
            rx.input(
                placeholder="Nombre",
                value=CustomersState.nombre,
                on_change=CustomersState.set_nombre,
            ),
            rx.input(
                placeholder="Apellido",
                value=CustomersState.apellido,
                on_change=CustomersState.set_apellido,
            ),
            rx.input(
                placeholder="Email (opcional)",
                value=CustomersState.email,
                on_change=CustomersState.set_email,
            ),
            rx.input(
                placeholder="Teléfono",
                value=CustomersState.telefono,
                on_change=CustomersState.set_telefono,
            ),
            rx.text_area(
                placeholder="Dirección",
                value=CustomersState.direccion,
                on_change=CustomersState.set_direccion,
            ),
            rx.hstack(
                rx.button(
                    rx.cond(
                        CustomersState.selected_id != None,
                        "Actualizar",
                        "Crear",
                    ),
                    color_scheme="orange",
                    on_click=CustomersState.save_customer,
                ),
                rx.button(
                    "Limpiar",
                    variant="soft",
                    on_click=CustomersState.clear_form,
                ),
                spacing="3",
            ),
            rx.cond(
                CustomersState.form_message != "",
                rx.text(CustomersState.form_message, color="orange.10"),
            ),
            spacing="3",
        ),
        bg="#fff8f0",
        border="1px solid #fed7aa",
        border_radius="1rem",
        padding="1.5rem",
        width="22rem",
    )


def filters_bar() -> rx.Component:
    """Barra de filtros arriba de la tabla."""
    return rx.hstack(
        rx.input(
            placeholder="Buscar por nombre o apellido...",
            value=CustomersState.search_name,
            on_change=CustomersState.set_search_name,
            width="16rem",
        ),
        rx.input(
            placeholder="Buscar por email...",
            value=CustomersState.search_email,
            on_change=CustomersState.set_search_email,
            width="16rem",
        ),
        rx.button(
            "Filtrar",
            color_scheme="orange",
            on_click=CustomersState.load_customers,
        ),
        rx.button(
            "Limpiar",
            variant="soft",
            on_click=CustomersState.clear_filters,
        ),
        spacing="3",
        wrap="wrap",
    )


def pagination_controls() -> rx.Component:
    """Botones de paginación."""
    return rx.hstack(
        rx.button("← Anterior", on_click=CustomersState.prev_page),
        rx.button("Siguiente →", on_click=CustomersState.next_page),
        spacing="4",
    )


# ===============================
# PÁGINA PRINCIPAL
# ===============================

def customers_page() -> rx.Component:
    """Vista principal del módulo Clientes."""
    return rx.vstack(
        rx.heading("Gestión de Clientes", size="6", color="orange.9"),
        rx.text("Consulta, crea o edita los clientes registrados en LootBox."),
        rx.divider(margin_y="0.5rem"),
        filters_bar(),
        customers_table(),
        pagination_controls(),
        rx.divider(margin_y="1rem"),
        customer_form(),
        spacing="4",
        width="100%",
        on_mount=CustomersState.load_customers,
    )
